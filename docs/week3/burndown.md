# Iteration 1 Burndown

## Iteration Scope

Iteration 1 contains three user stories with a total estimated effort of seven
development days.

| No. | User Story | Estimate |
| --- | --- | ---: |
| 01 | User Account Access | 2 days |
| 02 | Personal Reading List | 3 days |
| 03 | Reading Status Management | 2 days |
| **Total** |  | **7 days** |

## Daily Burndown Record

One development day represents approximately six focused hours. The daily
record follows the task sequence and estimates in the
[Iteration 1 Task Breakdown](../week4/task-breakdown.md).

| Course Point | Work Completed and Adjustment | Effort Burned | Ideal | Actual |
|---|---|---:|---:|---:|
| Week 3 Start | Scope approved; Stories 01–03 and their tasks entered as `todo` | 0.00 day | 7.00 | 7.00 |
| Week 3 Day 1 | Project and authentication configuration completed; registration and email validation implemented. Environment setup took longer than planned, so Story 01 remained `in-progress` | 0.75 day | 6.00 | 6.25 |
| Week 3 Day 2 | Login, logout, protected routes, account templates and authentication tests completed. Story 01 moved to `done`; Story 02 moved to `in-progress` | 1.25 days | 5.00 | 5.00 |
| Week 3 Day 3 | Book model, migration and routes completed. Form validation required additional review, leaving Story 02 slightly behind the ideal line | 0.75 day | 4.00 | 4.25 |
| Week 4 Day 1 | Book form validation completed and CRUD views advanced. Shared class-based view patterns reduced implementation risk | 1.00 day | 3.00 | 3.25 |
| Week 4 Day 2 | CRUD views, templates, owner-only access and isolation tests completed. Reuse of `OwnedBookQuerysetMixin` recovered the variance; Story 02 moved to `done` and Story 03 to `in-progress` | 1.25 days | 2.00 | 2.00 |
| Week 4 Day 3 | Reading-status choices, form selection and readable labels completed. Usability feedback identified the need for clearer guidance and visual treatment | 0.75 day | 1.00 | 1.25 |
| Week 5 Day 1 | Status styling, validation tests, form guidance, usability review and final acceptance completed. Story 03 moved to `done` and remaining effort reached zero | 1.25 days | 0.00 | 0.00 |

Story 01 reached `done` on Week 3 Day 2, Story 02 on Week 4 Day 2 and Story 03
on Week 5 Day 1. The final remaining effort was zero, so
Iteration 1 delivered all 7 estimated development-days without carry-over.

## Daily Agile Evidence

| Course Point | Story Status at End of Day | Main Repository Evidence |
|---|---|---|
| Week 3 Start | 01 `todo`; 02 `todo`; 03 `todo` | `763a331` — Iteration planning |
| Week 3 Day 1 | 01 `in-progress`; 02 `todo`; 03 `todo` | `71ae7d0` — Django project initialisation |
| Week 3 Day 2 | 01 `done`; 02 `in-progress`; 03 `todo` | `ce730a3` — Iteration 1 reading-management implementation |
| Week 3 Day 3 | 01 `done`; 02 `in-progress`; 03 `todo` | `ce730a3`, `7467500` — model/routes implementation and setup documentation |
| Week 4 Day 1 | 01 `done`; 02 `in-progress`; 03 `todo` | `ce730a3` — form and class-based view implementation |
| Week 4 Day 2 | 01 `done`; 02 `done`; 03 `in-progress` | `f0e1fdc` — automated coverage and owner-isolation checks |
| Week 4 Day 3 | 01 `done`; 02 `done`; 03 `in-progress` | `bc93f18` — focused form-guidance and usability improvement |
| Week 5 Day 1 | 01 `done`; 02 `done`; 03 `done` | PR #10 review and merge commit `9b2010f` |

The implementation commit `ce730a3` covers work completed across more than one
development day, so the Git history is less detailed than the burndown table.
For Iteration 2, the team will finish each active development day with one
scoped commit and a same-day issue and Project status update.

## Burndown Graph

![Iteration 1 burndown](../week6/iteration-1-burndown.svg)

The completed graph and its planning interpretation are included in the
[Practical 6 Report](../week6/practical-report.md).
