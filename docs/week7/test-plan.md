# Week 7 Test Plan

## Purpose

This plan applies Practical 7 test-driven-development principles to the
currently implemented Reading Compass release. It documents the tests that can
be performed now, the risks they address, and the automation approach used.

## Scope

The test scope is the completed account-access, personal-reading-list,
reading-status, progress, dashboard and reading-plan features. For
traceability, their acceptance behaviour is expressed as seven user stories:

1. **US7-01 — Account access:** As a reader, I want to register, sign in and
   sign out securely so that I can control access to my reading data.
2. **US7-02 — View my list:** As a reader, I want to see only my books so that
   my reading list remains private and useful.
3. **US7-03 — Add a book:** As a reader, I want to add a valid book so that I
   can build my reading list.
4. **US7-04 — Maintain books:** As a reader, I want to update and remove my
   own books so that my list remains accurate.
5. **US7-05 — Update progress:** As a reader, I want to update my current page
   so that I can see trustworthy reading progress.
6. **US7-06 — View dashboard:** As a reader, I want an owner-only view of my
   active books so that I can quickly understand current activity.
7. **US7-07 — Manage reading target:** As a reader, I want an optional target
   date so that I can plan without scheduling every book.

These stories are acceptance-level slices of backlog Stories 01–06.

## Test Types

| Type | Purpose | Examples |
|---|---|---|
| Model unit tests | Verify model defaults, validation, relationships and URL behaviour | positive page count, status default, owner cascade |
| Form unit tests | Verify normalisation and invalid-input handling independently of views | trimmed text, blank optional pages, unknown status |
| View integration tests | Exercise request, form, database, redirect and template behaviour together | registration, create, update and delete |
| Authentication tests | Verify session creation/termination and route protection | login, logout, `next` redirect |
| Authorisation tests | Verify object ownership boundaries | another user's book returns 404 |
| Boundary and negative tests | Verify empty, missing, duplicate, excessive and invalid values | missing email, 201-character title, zero pages |
| Presentation assertions | Verify important status, metadata, guidance and empty-state content | readable status label, missing-page message |

## Test Design Techniques

- **Equivalence partitioning:** valid and invalid login details; accepted and
  unrecognised reading statuses.
- **Boundary-value analysis:** page count `1` versus `0`; title length `200`
  versus `201`; current page equal to or above total; target today versus past.
- **Decision/permission testing:** anonymous, owner and non-owner access paths.
- **State-transition testing:** registration creates an authenticated session;
  login and logout change session state; status updates persist.
- **Error guessing:** duplicate email with different case, duplicate username,
  whitespace around text fields and GET requests to the POST-only logout view.

## Tools and Environment

| Item | Value |
|---|---|
| Framework | Django built-in `TestCase` test framework |
| Application dependency | Django `>=5.2,<5.3` |
| Database | Isolated in-memory SQLite test database |
| Test location | `books/tests.py` |
| Test command | `.venv/bin/python manage.py test -v 2` |
| Project time zone | Asia/Singapore |

Django creates and destroys the test database automatically. Tests do not
depend on the development database, execution order, external services or live
GitHub access.

## Entry and Exit Criteria

Entry criteria:

- dependencies are installed in `.venv`;
- migrations can be applied to the temporary test database;
- the baseline suite passes before test expansion.

Exit criteria:

- at least five user stories have at least three documented test cases each;
- at least 15 automated tests run;
- the complete suite passes with no Django system-check issues;
- documented test names and results match the implementation.

## Out of Scope

Backlog Stories 07–10 (search and filtering, notes, completion reviews and
duplicate warning) are not yet implemented on this branch. They should receive
their own failing tests first when their TDD implementation begins.

Manual usability, visual-regression, accessibility-tool, browser compatibility,
performance and security-penetration testing are also outside this automated
unit/integration suite. They remain useful follow-up activities.

## Risks and Controls

| Risk | Control |
|---|---|
| One reader accesses another reader's data | Owner-scoped list/detail/edit/delete tests |
| Invalid input corrupts reading data | Model, form and view negative tests |
| Authentication bypass exposes private routes | Anonymous redirect tests for every book route |
| Form behaviour and model rules drift apart | Both direct form tests and request-level tests |
| Test database affects development data | Django isolated test database |
| Documentation becomes inaccurate | Every case names its automated test method |
