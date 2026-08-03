# Story 08 — Private Reading Notes

## Week 9 Day 1

Story 08 began with executable acceptance tests before implementation. The
first run failed because `ReadingNote` did not exist, establishing the expected
TDD red state.

The acceptance suite covers:

- retaining a valid note on an owned book;
- rejecting blank content;
- editing and deleting an owned note;
- showing notes only within the owned book context;
- preventing creation, editing or deletion through another reader's records;
- requiring authentication on note routes; and
- cascading note deletion when the parent book is deleted.

## Model and Migration

Week 9 Day 1 adds `ReadingNote` with:

- an owning `Book` relationship and `notes` reverse relation;
- cascading deletion with its book;
- non-blank text content enforced by model validation and a database check;
- created and updated timestamps; and
- deterministic newest-updated-first ordering.

The three model tests pass. The migration plan creates the new model, and the
migration drift check reports no changes. Request-level tests remain red only
for the deliberately unimplemented note routes and book-detail interface,
which belong to Week 9 Day 2 and Week 9 Day 3.
