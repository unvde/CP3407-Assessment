# Iteration 2 Review

## Outcome

Iteration 2 is complete. Stories 04–06 passed acceptance at Week 7 Day 6 and
were merged to `main`. The iteration delivered the full adjusted scope without
carry-over.

| Story | Estimate | Result |
|---|---:|:---:|
| 04 — Reading Progress Updates | 3 development-days | done |
| 05 — Reading Dashboard | 2 development-days | done |
| 06 — Reading Plans | 2 development-days | done |
| **Total** | **7 development-days** | **7 done** |

## Actual Velocity

Velocity counts the estimates of accepted stories:

```text
3 + 2 + 2 = 7 development-days
```

The actual velocity is **7 development-days**, equal to the planned capacity.
No unfinished story is carried into Iteration 3.

## Acceptance Evidence

- Story 04 validates page bounds, calculates progress and preserves ownership.
- Story 05 requires login and shows only the reader's active books.
- Story 06 supports optional targets, rejects newly entered past targets and
  preserves owner isolation.
- The final Iteration 2 suite contained 32 passing automated tests.
- Completed-story evidence is recorded in the
  [Iteration 2 user-story pages](../week7/user-stories/README.md).

PR #31 received a detailed conversation review comment. GitHub records that
feedback as a PR conversation comment rather than a submitted review event;
this report preserves that distinction and does not claim a formal approval.

## Retrospective

### What worked

- Adjusting Story 05 kept the iteration within demonstrated capacity.
- Owner-scoped query reuse reduced security risk across the dashboard and CRUD.
- Tests exposed boundary and privacy failures before acceptance.
- Small feature commits made delivered scope easier to trace.

### What to improve

- Submit future reviews through GitHub's formal review control as well as the
  conversation.
- Update the central backlog at each acceptance checkpoint.
- Connect Project status, Issue labels and documentation in the same course-day
  close-out step.

### Iteration 3 actions

1. Begin every story with failing acceptance tests.
2. Keep all queries owner-scoped before adding search or feature filters.
3. Record status and remaining effort at every `Week X Day Y` checkpoint.
4. Reserve an explicit acceptance-review task for each story.

## Capacity Decision

Iteration 3 retains a 7-development-day capacity. Stories 07, 08 and 09 total
exactly 7 days. Story 10 remains in the backlog because adding it would exceed
the demonstrated velocity.
