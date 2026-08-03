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

## Week 9 Day 2

The owner-scoped note creation and editing workflow is implemented:

- `ReadingNoteForm` trims content and shows the required blank-note message;
- creation resolves the parent book through the authenticated owner before
  assigning the note;
- editing resolves notes only through books owned by the authenticated reader;
- successful create and edit requests return to the owned book detail;
- the book detail shows only notes attached to that already owner-scoped book;
- labelled create and edit controls are available; and
- anonymous create/edit requests redirect to sign in.

The seven Day 2 acceptance tests pass. Existing regression, model tests and the
implemented request scope pass 51 tests with a clean Django system check and no
migration drift. The complete Story 08 suite now has only three expected red
tests, all caused by the intentionally absent `note-delete` route scheduled for
Week 9 Day 3.
