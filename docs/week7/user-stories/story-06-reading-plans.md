# Story 06 — Reading Plans

**Estimate:** 2 development-days  
**Final status:** done at Week 7 Day 5

As a reader, I want to set an optional completion target so that I can plan my
reading without being forced to schedule every book.

## Acceptance Evidence

- `target_date` was added as an optional field in its own migration.
- Readers can add, change and remove a target on an owned book.
- Newly entered past targets are rejected; an unchanged historical target does
  not prevent edits to other book information.
- The detail page and dashboard display the target or a clear empty state.
- Owner-scoped views prevent another reader from seeing or changing the target.
- Reading-plan tests are documented as PLAN-01–PLAN-05 in the
  [Week 7 test cases](../test-cases.md).

The Week 7 Day 5 acceptance review found every criterion satisfied.
