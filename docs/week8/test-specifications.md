# Iteration 3 Test Specifications

These specifications are the TDD starting point. Each case should be written as
a failing test before its smallest implementation change. The existing 33-test
suite remains the regression baseline, including the deterministic mock-time
example.

## Story 07 — Search and Filtering

| ID | Given | When | Then |
|---|---|---|---|
| S07-01 | An owner has books with different titles | Search uses part of a title with different case | Matching owned books appear |
| S07-02 | An owner has books by different authors | Search uses part of an author | Matching owned books appear |
| S07-03 | Books have different statuses | A valid status is selected | Only that status appears |
| S07-04 | Search and status inputs are present | Both are applied | Results satisfy both constraints |
| S07-05 | Another reader has a matching book | The owner searches | The other reader's book is absent |
| S07-06 | Filters are active | Inputs are cleared | The full owned list returns |
| S07-07 | An unknown status is supplied | The list is requested | Input is safely ignored or rejected without data leakage |

## Story 08 — Private Reading Notes

| ID | Given | When | Then |
|---|---|---|---|
| S08-01 | A signed-in owner views an owned book | A valid note is submitted | The note is stored for that book and owner |
| S08-02 | An owned note exists | Its content is edited | The new content persists |
| S08-03 | An owned note exists | Delete is confirmed | The note is removed |
| S08-04 | Note content is blank | Create is submitted | Validation rejects it |
| S08-05 | Another reader owns a note | The current reader requests it | Response is not found and content is absent |
| S08-06 | A reader is anonymous | A note route is requested | Login is required |
| S08-07 | A book is deleted | Its notes exist | Notes are removed by the defined cascade |

## Story 09 — Completion Review

| ID | Given | When | Then |
|---|---|---|---|
| S09-01 | An owned book is completed | Valid rating, completion date and reflection are submitted | Review persists and displays |
| S09-02 | Rating is below or above the allowed range | Review is submitted | Validation rejects it |
| S09-03 | Completion date is in the future | Review is submitted | Validation rejects it using controlled time |
| S09-04 | Book status is not completed | Review is submitted | The workflow rejects or withholds the review |
| S09-05 | A review exists | Valid fields are updated | Updated values persist |
| S09-06 | Another reader owns the reviewed book | The current reader requests or posts | Response is not found and data is unchanged |
| S09-07 | Reflection is at its length boundary | Review is submitted | Boundary-valid text passes and over-limit text fails |

## Required Test Levels

- Model tests: relationships, cascade rules, rating/date/content validation.
- Form tests: boundary values and readable validation messages.
- View tests: authentication, ownership, persistence, redirects and templates.
- Query tests: combined filters and owner isolation.
- Regression: complete Django suite after every story.

## Entry and Exit Criteria

Entry requires an accepted Story Issue and at least one failing acceptance test.
Exit requires all mapped cases to pass, zero migration drift, a clean Django
system check, valid documentation links and recorded acceptance evidence.
