# Iteration 1 Completed User Stories

## 1. Delivered Solution

Iteration 1 delivered the first usable version of Reading Compass: an authenticated reader can maintain a private personal reading list and assign a controlled reading status to each book.

All three committed Iteration 1 user stories are complete.

## 2. User Story 01 — User Account Access

### User outcome

A reader can create an account, sign in, sign out and access private application pages securely.

### Delivered features

- registration form;
- unique email validation;
- login and logout;
- automatic login after registration;
- protected book pages for authenticated users.

### Acceptance evidence

- valid registrations create an account;
- duplicate email addresses are rejected;
- valid credentials allow login;
- invalid credentials do not allow login;
- logging out ends the authenticated session;
- unauthenticated users are redirected away from protected pages;
- related GitHub issues #1, #2 and #3 are closed.

## 3. User Story 02 — Personal Reading List

### User outcome

A signed-in reader can maintain a personal collection of books without exposing it to other users.

### Delivered features

- create a book;
- list the current user's books;
- view book details;
- edit a book;
- delete a book;
- record title, author and optional total pages;
- automatically assign the authenticated user as owner;
- restrict view, edit and delete access to the owner.

### Acceptance evidence

- created books are assigned to the current user on the server;
- each user sees only their own books;
- another user's book cannot be viewed, edited or deleted;
- valid CRUD operations are covered by automated tests;
- related GitHub issues #4, #5, #6 and #7 are closed.

## 4. User Story 03 — Reading Status Management

### User outcome

A reader can identify the current state of each book using consistent status choices.

### Delivered features

- Want to Read;
- Currently Reading;
- Paused;
- Completed;
- controlled database and form values;
- readable labels in the interface;
- explanatory guidance on add and edit forms.

### Acceptance evidence

- only defined status values are available through the form;
- saved status values are shown with readable labels;
- the add-book form explains the meaning of each status;
- the usability review was completed;
- pull request #10 was reviewed and merged;
- related GitHub issues #8 and #9 are closed.

## 5. Quality and Technical Evidence

Iteration 1 also produced the following supporting evidence:

- class diagram for the implemented Django classes;
- sequence diagram for adding a book;
- automated tests for authentication, book management and privacy;
- a focused usability improvement through a feature branch and pull request;
- task tracking through GitHub issues and status labels;
- SRP and DRY review of the delivered code.

## 6. Completion Summary

| User Story | Estimate | Status | Main Evidence |
| --- | ---: | --- | --- |
| User Account Access | 2 days | Completed | Authentication workflows, tests, issues #1–#3 |
| Personal Reading List | 3 days | Completed | Book CRUD, owner isolation, tests, issues #4–#7 |
| Reading Status Management | 2 days | Completed | Controlled statuses, guidance, PR #10, issues #8–#9 |
| **Total** | **7 days** | **Completed** | **100% of Iteration 1 scope** |

The resulting actual Iteration 1 velocity is **7 estimated development days**.
