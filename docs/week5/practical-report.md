# Practical 5 Report

## Iteration 1 — Reflection and Closure

## 1. Objective

The objective of Practical 5 is to reflect on Iteration 1 and record its final design quality, tracking status, completed and unfinished user stories, delivered user-story pages and actual velocity.

## 2. Practical Requirements and Evidence

| Practical 5 Task | Result | Evidence |
| --- | --- | --- |
| Check classes against SRP and DRY | Completed | [SRP and DRY Review](srp-dry-review.md) |
| Monitor tasks and user stories using `todo`, `in-progress` and `done` | Completed for Iteration 1 closure | Nine GitHub issues closed and Iteration 1 Project items recorded as Done |
| Document completed and unfinished user stories | Completed | [Iteration 1 Retrospective](iteration1-retrospective.md) |
| Update GitHub pages for each completed user story | Completed | [Completed User Stories](completed-user-stories.md) |
| Calculate actual Iteration 1 velocity | Completed | **7 estimated development days** |

## 3. SRP and DRY Review

The Iteration 1 code generally satisfies both principles.

Key findings:

- the `Book` model remains focused on book data and domain behaviour;
- `RegistrationForm` and `BookForm` contain their related validation rules;
- each class-based view coordinates one workflow;
- `OwnedBookQuerysetMixin` centralises owner-only data filtering;
- create and update workflows reuse `BookForm`;
- templates reuse the shared `base.html` layout;
- Django generic views and authentication components prevent unnecessary framework-code duplication.

No major violation requires immediate refactoring. Minor future improvements are documented in the full [SRP and DRY Review](srp-dry-review.md).

## 4. Task and User-Story Tracking

Iteration 1 work is represented by nine GitHub issues. At closure, all nine issues are closed and the corresponding work is treated as Done.

| Issue Group | User Story | Final Status |
| --- | --- | --- |
| Issues #1–#3 | User Account Access | Done |
| Issues #4–#7 | Personal Reading List | Done |
| Issues #8–#9 | Reading Status Management | Done |

The repository uses the required workflow vocabulary:

- `todo` — planned and not started;
- `in-progress` — actively being implemented, tested or reviewed;
- `done` — acceptance conditions met with supporting evidence.

The issues were created retrospectively during Practical 4. This limitation is recorded openly; future iteration issues should be created and moved through statuses while the work is being performed.

## 5. Completed Versus Unfinished Stories

| Category | Stories | Estimate |
| --- | ---: | ---: |
| Completed | 3 | 7 days |
| Unfinished | 0 | 0 days |
| Partially completed | 0 | 0 days |

Completed stories:

1. User Account Access.
2. Personal Reading List.
3. Reading Status Management.

Detailed delivered outcomes and acceptance evidence are provided in [Completed User Stories](completed-user-stories.md).

## 6. Actual Velocity

The actual velocity is the total original estimate of user stories completed to the agreed definition of done.

```text
Actual Velocity = 2 days + 3 days + 2 days
                = 7 estimated development days
```

| Metric | Value |
| --- | ---: |
| Planned workload | 7 days |
| Completed workload | 7 days |
| Actual velocity | **7 days/iteration** |
| Completion rate | **100%** |
| Story-level variance | **0 days** |

The nine GitHub issue estimates total five days because those issues are grouped retrospective tracking records and do not represent every task contained in the original seven-day story estimates. The full reconciliation is documented in [Iteration 1 Retrospective](iteration1-retrospective.md).

## 7. Delivered Evidence

Iteration 1 completion is supported by:

- implemented registration, login and logout workflows;
- private book CRUD functionality;
- owner-only data access;
- controlled reading statuses;
- automated test coverage;
- class and sequence diagrams;
- nine closed task issues;
- merged pull request #10 following usability review;
- Week 4 execution and tracking documentation;
- Week 5 SRP, DRY, completion and velocity documentation.

## 8. Reflection

Iteration 1 delivered the full committed scope. The main technical strengths are reuse of Django framework components, centralised ownership filtering and automated coverage of security-sensitive behaviour.

The main process weakness is that detailed issue tracking was created after much of the implementation had already occurred. This makes the final state visible but provides weaker evidence of real-time agile tracking. Iteration 2 should begin with issues, estimates, assignments and statuses already established.

## 9. Actions for Iteration 2

- use 7 development days as the initial capacity reference;
- select stories within that capacity;
- create and estimate task issues before development;
- back-check task totals against parent-story estimates;
- update statuses as work progresses;
- collect acceptance and test evidence for each completed story;
- maintain remaining-work data for a burndown graph.

## 10. Completion Checklist

- [x] Review classes for SRP.
- [x] Review implementation for DRY.
- [x] Record findings.
- [x] Confirm final task and story statuses.
- [x] Document completed stories.
- [x] Document unfinished stories.
- [x] Prepare a page for each completed Iteration 1 story.
- [x] Calculate actual Iteration 1 velocity.
- [x] Reconcile task-level and story-level estimates.
- [x] Record improvements for Iteration 2.

## 11. Conclusion

Practical 5 is complete at the documentation level. All three Iteration 1 user stories were completed, producing an actual velocity of **7 estimated development days per iteration**. The next priority is to use this result to plan and track Iteration 2 more consistently.
