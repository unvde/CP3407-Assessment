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
