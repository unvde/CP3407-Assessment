# Story 02 — Personal Reading List

## User Story

As a reader, I want to maintain a personal reading list so that I can keep books
that interest me in one organised location.

**Estimate:** 3 days  
**Iteration:** 1  
**Status:** done

## Completed Behaviour

- A signed-in reader can add a book with title, author, status and optional
  positive page count.
- The reader can view their list and individual book details.
- Existing entries can be edited or deleted with confirmation.
- Every saved book is assigned to the authenticated owner on the server.
- Readers cannot view, edit or delete another reader's entries.

## Acceptance Evidence

Automated tests cover list isolation, owner assignment, positive-page
validation, update, delete and denial of cross-user view, edit and delete
requests.

## Main Implementation

- `Book` stores owner and bibliographic fields.
- `BookForm` validates editable input.
- Separate class-based views implement list, detail, create, update and delete.
- `OwnedBookQuerysetMixin` centralises owner-scoped access.
