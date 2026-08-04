# Story 02 — Shared Catalogue Search and Import

**Issue:** [#2](https://github.com/unvde/CP3407-Assessment/issues/2)

**Iteration:** 1 · **Estimate:** 3 development-days · **Status:** Done

## Delivered behaviour

- Search Open Library by title, author or ISBN.
- Normalise results and rank exact canonical editions before noisy duplicates.
- Import through a signed token that rejects tampering.
- Reuse existing `CatalogBook` records and avoid duplicate shelf entries.
- Preserve a manual-add route and controlled error state when the API is unavailable.

## Implementation and tests

- Implementation: `books/services.py`, `BookSearchView`, `BookImportView`, `CatalogBook` and `Book`.
- Automated evidence: `OpenLibraryServiceTests` and `BookImportTests` in `books/test_community.py`.
- External requests are mocked, keeping tests deterministic and network-independent.

## Acceptance

The live Find a book page provides title/author/ISBN search and credits Open Library. Imported catalogue data is shared while the reader's shelf status remains private.
