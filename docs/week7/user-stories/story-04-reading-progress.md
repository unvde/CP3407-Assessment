# Story 04 — Reading Progress Updates

**Estimate:** 3 development-days  
**Final status:** done at Week 7 Day 3

As a reader, I want to update my current reading position so that I can see how
much of a book I have completed.

## Acceptance Evidence

- `current_page` was added in its own migration with a non-negative field type.
- Model and form validation reject progress above a known total page count.
- The list, detail page and dashboard show current page and calculated progress.
- A missing total shows “Percentage unavailable” rather than a misleading value.
- Owner-scoped views return 404 for another reader's book.
- Progress tests are documented as PROG-01–PROG-04 in the
  [Week 7 test cases](../test-cases.md).

The Week 7 Day 3 acceptance review found every criterion satisfied.
