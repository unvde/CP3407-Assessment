# Story 03 — Personal Shelf and Reading Statuses

**Issue:** [#3](https://github.com/unvde/CP3407-Assessment/issues/3)

**Iteration:** 1 · **Estimate:** 2 development-days · **Status:** Done

## Delivered behaviour

- Each shelf entry belongs to exactly one authenticated reader.
- Status is restricted to Want to Read, Currently Reading, Paused or Completed.
- Readers can filter their shelf and update status directly.
- Readers can create, edit and delete private notes.
- Cross-reader access returns 404 and private notes never appear on public pages.

## Implementation and tests

- Implementation: `Book`, `ReadingNote`, owner-scoped views, status update and note workflows.
- Automated evidence: `BookManagementTests`, `BookSearchAndFilterAcceptanceTests` and `PrivateReadingNoteAcceptanceTests`.
- System evidence: the owner-boundary and anonymous-write scenarios in `books/test_system.py`.

## Acceptance

The deployed My books and book-detail pages demonstrate owner-scoped shelf records, immediate status changes and private reflection notes.
