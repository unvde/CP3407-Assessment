# Story 09 — Completion Review

## Week 9 Day 4

Story 09 began with executable model and request acceptance tests before
implementation. The first run produced 11 expected errors because the review
fields, model time collaborator and review route did not exist.

The acceptance suite covers:

- retaining a rating, completion date and reflection on a completed book;
- accepting only ratings from 1 to 5;
- rejecting a completion date after the controlled course day;
- preventing review data on a book that is not completed;
- accepting a 1000-character reflection and rejecting 1001 characters;
- creating and updating a review through an owner-scoped workflow;
- returning not found for another reader's book;
- requiring authentication; and
- displaying review data only on the owned completed book detail.

## Data and Migration

Week 9 Day 4 adds optional `Book` fields for:

- a rating from 1 to 5;
- a completion date; and
- a reflection with a 1000-character limit.

Model validation permits review data only when the book status is Completed and
rejects completion dates after `timezone.localdate()`. Tests patch that time
collaborator with `date.min` or `date.max`, so no real date is recorded.

The first boundary run showed that `TextField(max_length=1000)` did not by
itself enforce length during model `full_clean()`. An explicit
`MaxLengthValidator(1000)` was therefore added to make the model-level rule
executable.

All five model tests now pass. Existing regression plus the implemented Story
09 model scope passes 59 tests, Django system check reports no issues and the
migration drift check reports no changes. Six tests remain red for the
deliberately unimplemented Week 9 Day 5 review route, form and detail display.

## Week 9 Day 5

The completion-review workflow is implemented:

- `CompletionReviewForm` requires a rating, completion date and reflection;
- the form provides the 1–5 and 1000-character boundaries;
- completion dates are checked at both form and model levels against the
  controlled course-day collaborator;
- the update view selects only completed books owned by the authenticated
  reader;
- the same workflow creates the first review and updates an existing review;
- non-completed and cross-reader book requests return not found;
- anonymous access redirects to sign in; and
- the completed owned book detail provides add/edit controls and renders the
  private rating, completion date and reflection.

The workflow tests initially expected one time-collaborator call. The spy showed
two calls because form validation and model validation each enforce the date
boundary. The expectation was corrected to verify both layers explicitly.

## Acceptance Result

| Criterion | Evidence | Result |
|---|---|:---:|
| Store review data | Valid rating, controlled completion date and reflection persist | Pass |
| Validate rating | Values below 1 and above 5 are rejected | Pass |
| Validate completion date | A date after the controlled course day is rejected | Pass |
| Require completed status | A non-completed book cannot enter the review workflow | Pass |
| Update a review | Existing review values can be replaced and persist | Pass |
| Preserve privacy | Cross-reader requests return 404 and do not change data | Pass |
| Display the review | Unique review text appears only on the owned completed book detail | Pass |
| Enforce reflection boundary | 1000 characters pass and 1001 characters fail | Pass |

The complete Django suite passes all 65 tests. Django system check reports no
issues, and the migration drift check reports no changes. Story 09 therefore
meets its definition of done.
