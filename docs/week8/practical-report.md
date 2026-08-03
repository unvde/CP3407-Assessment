# Practical 8 Report

## Objective

Practical 8 closes Iteration 2, calculates actual velocity, records its
burndown and retrospective, then adjusts and starts Iteration 3 with a test-first
plan.

## Iteration 2 Close-Out

Stories 04–06 are accepted with no carry-over. Their estimates total **7
development-days**, so Iteration 2 actual velocity is **7 development-days**.
The detailed calculation and reflection are in the
[Iteration 2 review](iteration-2-review.md), and the course-day-only trend is in
the [Iteration 2 burndown](iteration-2-burndown.md).

The central requirements backlog now records Stories 04–06 as `done`. README
status and Week 8 navigation have also been reconciled with the accepted state.
Completed-story links use repository-relative paths and therefore resolve on
`main`, not an obsolete feature branch.

## Iteration 3 Adjustment

The new capacity remains 7 development-days:

| Story | Estimate | Decision |
|---|---:|---|
| 07 — Search and Filtering | 2 | committed |
| 08 — Private Reading Notes | 3 | committed |
| 09 — Completion Review | 2 | committed |
| 10 — Duplicate Book Warning | 1 | product backlog |

The [Iteration 3 plan](iteration-3-plan.md) defines acceptance criteria,
schedule and Definition of Done. The
[initial burndown](iteration-3-burndown.md) begins at 7 days on Week 8 Day 1.

## Tracking Structure

Story Issues #32–#34 and task Issues #35–#47 are open, assigned and labelled
`todo`. The [project-board document](iteration-3-project-board.md) records the
initial 3-story, 13-task snapshot and explains the current GitHub Projects
integration limitation.

## TDD and Mock Objects

The [test specifications](test-specifications.md) define 21 acceptance cases
covering success, validation, authentication, owner isolation and boundary
conditions. The implementation sequence is red, green, refactor, then full
regression.

The [mock-object research](mock-object-research.md) distinguishes mocks from
other test doubles and identifies time as a suitable deterministic boundary.
A passing test patches the form's local-date collaborator and verifies both the
validation outcome and the interaction.

## Completion Checklist

- Iteration 2 review and retrospective completed.
- Actual velocity calculated as 7 development-days.
- Iteration 2 burndown recorded without calendar dates.
- Iteration 3 scope adjusted to demonstrated velocity.
- Story and task Issues created with owners and workflow labels.
- Initial project-board and burndown records completed.
- Mock-object research and executable example completed.
- Iteration 3 TDD specifications completed.
- Backlog and README status reconciled.

Iteration 2 is formally closed and Iteration 3 is ready to begin implementation.
