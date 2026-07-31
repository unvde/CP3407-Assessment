# Iteration Plan

## 1. Milestone Overview

The Reading Compass requirements backlog contains ten user stories with a combined estimated effort of 23 development days.

The stories are divided into three iterations according to priority, effort and technical dependencies.

## 2. Iteration 1 — Core Reading Management

**Iteration Goal:** Deliver a secure minimum reading-list workflow in which users can access an account, manage personal book records and assign reading statuses.

| No. | User Story | Priority | Estimate |
| --- | --- | --- | --- |
| 01 | User Account Access | 10 | 2 days |
| 02 | Personal Reading List | 10 | 3 days |
| 03 | Reading Status Management | 10 | 2 days |
| **Total** |  |  | **7 days** |

### Expected Outcome

At the end of Iteration 1, a user should be able to:

- Register an account
- Sign in and sign out
- View a private reading list
- Add, view, edit and delete personal book records
- Assign a reading status to each book
- Access only their own reading information

## 3. Iteration 2 — Reading Plans and Progress

**Iteration Goal:** Allow users to plan their reading, record progress and view an activity summary.

| No. | User Story | Priority | Estimate |
| --- | --- | --- | --- |
| 04 | Reading Progress Updates | 10 | 3 days |
| 05 | Reading Dashboard | 20 | 2 days |
| 06 | Reading Plans | 20 | 2 days |
| **Total** |  |  | **7 days** |

Reading Progress Updates has priority 10 but depends on the account and book-management functionality delivered in Iteration 1.

Week 6 adjusted the original 8-day plan to the demonstrated Iteration 1
velocity of 7 estimated development-days. The first dashboard release is
restricted to active books, progress and optional targets. See the
[Practical 6 Report](../week6/practical-report.md).

## 4. Iteration 3 — Reading Support Features

**Iteration Goal:** Improve the usefulness and organisation of the reading experience.

| No. | User Story | Priority | Estimate |
| --- | --- | --- | --- |
| 07 | Search and Filtering | 30 | 2 days |
| 08 | Private Reading Notes | 30 | 3 days |
| 09 | Completion Review | 40 | 2 days |
| 10 | Duplicate Book Warning | 50 | 1 day |
| **Total** |  |  | **8 days** |

## 5. Milestone Summary

| Iteration | Goal | Estimated Effort |
| --- | --- | --- |
| 1 | Core reading management | 7 days |
| 2 | Reading plans and progress | 7 days |
| 3 | Reading support features | 8 days |
| **Total** |  | **22 days** |

## 6. Planning Rationale

The implementation order prioritises the minimum usable product while respecting technical dependencies.

Account and book-management functionality must exist before progress, planning, dashboard, note and review features can be implemented. Lower-priority enhancements are therefore scheduled after the core workflow becomes stable.
