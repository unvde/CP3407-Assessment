# Iteration 3 Plan

## Goal and Capacity

Iteration 3 will make the personal library easier to navigate and support
private reflection after and during reading. Capacity is based on the Iteration
2 actual velocity of **7 development-days**.

| Story | Priority | Estimate | Issue | Initial status |
|---|:---:|---:|---|:---:|
| 07 — Search and Filtering | 30 | 2 days | [#32](https://github.com/unvde/CP3407-Assessment/issues/32) | todo |
| 08 — Private Reading Notes | 30 | 3 days | [#33](https://github.com/unvde/CP3407-Assessment/issues/33) | todo |
| 09 — Completion Review | 40 | 2 days | [#34](https://github.com/unvde/CP3407-Assessment/issues/34) | todo |
| **Total** |  | **7 days** |  |  |

Story 10 — Duplicate Book Warning remains in the product backlog. Its 1-day
estimate would exceed the demonstrated capacity and it is not an Iteration 3
commitment.

## Acceptance Summary

### Story 07

- case-insensitive title or author search;
- validated reading-status filter;
- combined search and filter;
- owner-only results; and
- clearing inputs restores the full personal list.

### Story 08

- create, edit and delete notes on an owned book;
- reject blank content;
- show notes only in the owning reader's book context; and
- prevent anonymous and cross-user access.

### Story 09

- store rating, completion date and reflection for a completed owned book;
- validate rating and date;
- update and display the review; and
- prevent cross-user access.

## Course-Day Schedule

| Course Point | Planned work | Planned remaining |
|---|---|---:|
| Week 8 Day 1–4 | Close Iteration 2; plan Iteration 3; prepare issues, research and TDD specifications | 7 days |
| Week 8 Day 5 | Implement and accept Story 07 | 5 days |
| Week 9 Day 1 | Specify Story 08 tests; add the reading-note model and migration | 4 days |
| Week 9 Day 2 | Implement private-note create and edit workflows | 3.25 days |
| Week 9 Day 3 | Complete note deletion, privacy controls and Story 08 acceptance | 2 days |
| Week 9 Day 4 | Specify Story 09 tests; add completion-review data and migration | 1 day |
| Week 9 Day 5 | Implement and accept Story 09 | 0 days |
| Week 9 Day 6 | Defect tracking, system testing and final Iteration 3 acceptance records | 0 days |

## Definition of Done

A story is `done` only when its acceptance tests pass, owner isolation is
verified, migrations show no drift, Django system checks pass, documentation
links are valid, its Issue tasks are closed and acceptance evidence is recorded.
