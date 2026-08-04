# Mock Object Research

## Purpose

A mock object replaces a collaborator with a controlled test double. It is most
useful at slow or non-deterministic boundaries such as an external API. It is
not a substitute for testing Django models, queries, permissions and views
against the isolated test database.

## Test-Double Vocabulary

- **Stub:** returns a prepared value.
- **Spy:** records how it was called.
- **Mock:** combines controlled behaviour with interaction expectations.
- **Fake:** provides a lightweight working implementation, such as Django's
  test email backend or test database.

## Reading Compass Boundaries

The application keeps Open Library communication in `books.services`. Service
tests patch `books.services.urlopen` because that is the name used by the code
under test. The prepared response behaves as a context manager and contains
realistic JSON, so ranking, normalisation, ISBN selection and duplicate removal
still run as production code.

```python
@patch("books.services.urlopen")
def test_search_parses_results_using_explicit_certificate_context(self, urlopen):
    urlopen.return_value = io.BytesIO(
        json.dumps({"docs": [{
            "key": "/works/OL893415W",
            "title": "Dune",
            "author_name": ["Frank Herbert"],
            "isbn": ["9780441172719"],
        }]}).encode()
    )

    results = search_open_library("Dune")

    self.assertEqual(results[0].title, "Dune")
    _, kwargs = urlopen.call_args
    self.assertEqual(kwargs["timeout"], 8)
    self.assertIsNotNone(kwargs["context"])
```

View tests patch the imported service name in `books.views`. This isolates view
behaviour from the network while retaining real requests, authentication,
messages, templates and database writes.

```python
@patch("books.views.search_open_library")
def test_search_displays_api_results(self, search):
    search.return_value = [self.result]

    response = self.client.get(reverse("book-search"), {"q": "Dune"})

    self.assertContains(response, "Dune")
    self.assertContains(response, "9780441172719")
    search.assert_called_once_with("Dune")
```

Discovery tests apply the same pattern to
`books.views.search_open_library_subject`. They cover successful remote
results, temporary failures and the local-catalogue fallback without making the
suite depend on internet availability.

## What Remains Real

- Model validation and database constraints.
- Authentication, owner scoping and staff permissions.
- Signed import token verification.
- Catalogue, shelf, review, list and forum persistence.
- Response status, redirects, messages and rendered content.

Keeping these collaborators real is important because replacing them would
hide integration errors in the behaviour the application owns.

## Rules Used by the Test Suite

- Patch the symbol where the production code looks it up.
- Use realistic external payloads, including missing and duplicate fields.
- Assert user-visible outcomes before optional call details.
- Cover success, HTTP/network failure, timeout and invalid-response paths at the
  service boundary.
- Keep view tests deterministic by preventing live network access.
- Retain end-to-end Django workflow tests for the data written after a mocked
  search result is returned.
