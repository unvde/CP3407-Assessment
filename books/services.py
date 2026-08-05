import json
import logging
import re
import ssl
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi
from django.conf import settings
from django.core import signing


OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPEN_LIBRARY_SUBJECT_URL = "https://openlibrary.org/subjects"
IMPORT_SALT = "reading-compass.book-import"
logger = logging.getLogger(__name__)


class BookSearchError(Exception):
    """Raised when the external book catalogue cannot be reached."""


@dataclass
class BookSearchResult:
    title: str
    author: str
    open_library_key: str
    isbn_10: str = ""
    isbn_13: str = ""
    cover_url: str = ""
    publisher: str = ""
    published_year: int | None = None
    categories: tuple[str, ...] = ()

    @property
    def import_token(self):
        return signing.dumps(asdict(self), salt=IMPORT_SALT, compress=True)

    @property
    def recommendation_identifier(self):
        identity = self.open_library_key or self.isbn_13 or self.isbn_10
        if not identity:
            identity = _normalise_search_text(f"{self.title} {self.author}")
        return f"openlibrary:{identity}"[:100]


def _first(values, default=""):
    return values[0] if isinstance(values, list) and values else default


def _clean_isbn(value):
    return re.sub(r"[^0-9Xx]", "", str(value or "")).upper()


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _clean_year(value):
    try:
        year = int(value)
    except (TypeError, ValueError):
        return None
    return year if 0 < year <= 32_767 else None


def _require_mapping_list(payload, key):
    if not isinstance(payload, dict) or not isinstance(payload.get(key, []), list):
        logger.warning("Open Library returned an unexpected response structure.")
        raise BookSearchError("Book search is temporarily unavailable.")
    return payload.get(key, [])


def _normalise_search_text(value):
    return " ".join(re.findall(r"[a-z0-9]+", (value or "").casefold()))


def _result_score(result, query, edition_count=0):
    clean_query = _normalise_search_text(query)
    isbn_query = _clean_isbn(query)
    if isbn_query and len(isbn_query) in {10, 13}:
        return 10_000 if isbn_query in {result.isbn_10, result.isbn_13} else -1

    title = _normalise_search_text(result.title)
    author = _normalise_search_text(result.author)
    categories = [_normalise_search_text(value) for value in result.categories]
    if not clean_query:
        return -1
    popularity_bonus = min(max(int(edition_count or 0), 0), 300)
    if title == clean_query:
        return 1_000 + popularity_bonus
    score = 0
    if title.startswith(clean_query):
        score += 600
    elif clean_query in title:
        score += 450
    if author == clean_query:
        score += 500
    elif clean_query in author:
        score += 300
    if clean_query in categories:
        score += 500
    query_tokens = set(clean_query.split())
    matched_tokens = query_tokens & set(
        f"{title} {author} {' '.join(categories)}".split()
    )
    score += 120 * len(matched_tokens)
    score += int(SequenceMatcher(None, clean_query, title).ratio() * 100)
    return score if matched_tokens or score >= 250 else -1


def search_open_library(query, limit=12, page=1, subject=None):
    query = query.strip()
    if not query:
        return []

    page = max(int(page or 1), 1)
    relevance_query = subject.strip() if subject else query
    api_query = f'subject:"{relevance_query}"' if subject else query

    params = urlencode(
        {
            "q": api_query,
            "page": page,
            "limit": limit if subject else min(max(limit * 4, 20), 50),
            "fields": (
                "key,title,author_name,isbn,cover_i,publisher,"
                "first_publish_year,subject,edition_count"
            ),
        }
    )
    request = Request(
        f"{OPEN_LIBRARY_SEARCH_URL}?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": getattr(
                settings,
                "OPEN_LIBRARY_USER_AGENT",
                "ReadingCompass/1.0 (student project)",
            ),
        },
    )
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        with urlopen(request, timeout=8, context=ssl_context) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        logger.warning("Open Library search failed: %s", exc)
        raise BookSearchError("Book search is temporarily unavailable.") from exc

    documents = _require_mapping_list(payload, "docs")
    ranked_results = []
    seen = set()
    for item in documents:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        isbns = [_clean_isbn(value) for value in _as_list(item.get("isbn"))]
        isbn_13 = next((value for value in isbns if len(value) == 13), "")
        isbn_10 = next((value for value in isbns if len(value) == 10), "")
        cover_id = item.get("cover_i")
        subjects = tuple(
            dict.fromkeys(
                str(value).strip()[:80]
                for value in _as_list(item.get("subject"))[:8]
                if str(value).strip()
            )
        )
        result = BookSearchResult(
                title=title[:200],
                author=", ".join(
                    str(value).strip()
                    for value in _as_list(item.get("author_name"))
                    if str(value).strip()
                )[:200]
                or "Unknown author",
                open_library_key=str(item.get("key", "")).replace("/works/", "")[:40],
                isbn_10=isbn_10,
                isbn_13=isbn_13,
                cover_url=(
                    f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    if cover_id
                    else ""
                ),
                publisher=str(_first(_as_list(item.get("publisher"))))[:200],
                published_year=_clean_year(item.get("first_publish_year")),
                categories=subjects,
            )
        dedupe_key = (
            result.open_library_key
            or result.isbn_13
            or result.isbn_10
            or f"{_normalise_search_text(result.title)}:{_normalise_search_text(result.author)}"
        )
        if dedupe_key in seen:
            continue
        score = _result_score(
            result, relevance_query, item.get("edition_count", 0)
        )
        if score < 0:
            continue
        seen.add(dedupe_key)
        ranked_results.append((score, result))
    ranked_results.sort(key=lambda item: (-item[0], item[1].title.casefold()))
    return [result for _, result in ranked_results[:limit]]


def search_open_library_subject(subject, limit=10, page=1):
    subject = " ".join(subject.strip().split())
    if not subject:
        return []
    page = max(int(page or 1), 1)
    subject_key = re.sub(r"[^a-z0-9]+", "_", subject.casefold()).strip("_")
    if not subject_key:
        return []
    params = urlencode({"limit": limit, "offset": (page - 1) * limit})
    request = Request(
        f"{OPEN_LIBRARY_SUBJECT_URL}/{subject_key}.json?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": getattr(
                settings,
                "OPEN_LIBRARY_USER_AGENT",
                "ReadingCompass/1.0 (student project)",
            ),
        },
    )
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        with urlopen(request, timeout=6, context=ssl_context) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        logger.warning("Open Library subject search failed: %s", exc)
        raise BookSearchError("Book search is temporarily unavailable.") from exc

    works = _require_mapping_list(payload, "works")
    results = []
    seen = set()
    for item in works:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        work_key = str(item.get("key", "")).replace("/works/", "")[:40]
        if not title or not work_key or work_key in seen:
            continue
        seen.add(work_key)
        cover_id = item.get("cover_id")
        author_names = [
            str(author.get("name", "")).strip()
            for author in _as_list(item.get("authors"))
            if isinstance(author, dict) and str(author.get("name", "")).strip()
        ]
        categories = tuple(
            dict.fromkeys(
                [subject]
                + [
                    str(value).strip()[:80]
                    for value in _as_list(item.get("subject"))[:3]
                    if str(value).strip()
                ]
            )
        )
        results.append(
            BookSearchResult(
                title=title[:200],
                author=", ".join(author_names)[:200] or "Unknown author",
                open_library_key=work_key,
                cover_url=(
                    f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    if cover_id
                    else ""
                ),
                published_year=_clean_year(item.get("first_publish_year")),
                categories=categories,
            )
        )
    return results


def load_import_token(token, max_age=3600):
    data = signing.loads(token, salt=IMPORT_SALT, max_age=max_age)
    allowed = {
        "title",
        "author",
        "open_library_key",
        "isbn_10",
        "isbn_13",
        "cover_url",
        "publisher",
        "published_year",
        "categories",
    }
    return {key: value for key, value in data.items() if key in allowed}
