import json
import logging
import re
import ssl
from dataclasses import asdict, dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi
from django.conf import settings
from django.core import signing


OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
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


def _first(values, default=""):
    return values[0] if isinstance(values, list) and values else default


def _clean_isbn(value):
    return re.sub(r"[^0-9Xx]", "", value or "").upper()


def search_open_library(query, limit=12):
    query = query.strip()
    if not query:
        return []

    params = urlencode(
        {
            "q": query,
            "limit": min(limit, 20),
            "fields": (
                "key,title,author_name,isbn,cover_i,publisher,"
                "first_publish_year,subject"
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

    results = []
    for item in payload.get("docs", []):
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        isbns = [_clean_isbn(value) for value in item.get("isbn", [])]
        isbn_13 = next((value for value in isbns if len(value) == 13), "")
        isbn_10 = next((value for value in isbns if len(value) == 10), "")
        cover_id = item.get("cover_i")
        subjects = tuple(
            dict.fromkeys(
                str(value).strip()[:80]
                for value in item.get("subject", [])[:8]
                if str(value).strip()
            )
        )
        results.append(
            BookSearchResult(
                title=title[:200],
                author=", ".join(item.get("author_name", []))[:200]
                or "Unknown author",
                open_library_key=str(item.get("key", "")).replace("/works/", "")[:40],
                isbn_10=isbn_10,
                isbn_13=isbn_13,
                cover_url=(
                    f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    if cover_id
                    else ""
                ),
                publisher=str(_first(item.get("publisher", [])))[:200],
                published_year=item.get("first_publish_year"),
                categories=subjects,
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
