# Iteration 1 Retrospective and Velocity Report

## 1. Purpose

This report closes Iteration 1 of Reading Compass by recording completed and unfinished user stories, calculating actual velocity, reviewing estimate accuracy, and identifying improvements for the next iteration.

## 2. Iteration 1 Scope

Iteration 1 contained three user stories with a total planned estimate of seven development days.

| No. | User Story | Planned Estimate | Final Status |
| --- | --- | ---: | --- |
| 01 | User Account Access | 2 days | Completed |
| 02 | Personal Reading List | 3 days | Completed |
| 03 | Reading Status Management | 2 days | Completed |
| **Total** |  | **7 days** | **Completed** |

## 3. Completed User Stories

### 3.1 User Story 01 — User Account Access

**Status:** Completed  
**Estimate:** 2 development days

Delivered outcomes:

- account registration;
- required email validation and duplicate-email rejection;
- login and logout;
- automatic login following successful registration;
- protection of private application routes;
- automated coverage of authentication and protected-route behaviour.

Completion evidence includes the Iteration 1 implementation commit, automated tests, closed GitHub issues #1–#3, and the completed account workflows in the application.

### 3.2 User Story 02 — Personal Reading List

**Status:** Completed  
**Estimate:** 3 development days

Delivered outcomes:

- `Book` model and database migration;
- private list of books for each authenticated user;
- create, view, update and delete workflows;
- server-side ownership assignment;
- owner-only access to book records;
- validation of editable book fields;
- automated tests for CRUD behaviour and cross-user isolation.

Completion evidence includes the Iteration 1 implementation and test commits and closed GitHub issues #4–#7.

### 3.3 User Story 03 — Reading Status Management

**Status:** Completed  
**Estimate:** 2 development days

Delivered outcomes:

- controlled status values: Want to Read, Currently Reading, Paused and Completed;
- status selection on book forms;
- readable status labels in the interface;
- guidance explaining each reading-status choice;
- automated validation and interface coverage;
- usability and acceptance review completed through pull request #10.

Completion evidence includes closed GitHub issues #8–#9 and the merged pull request **Improve Iteration 1 form guidance and usability**.

## 4. Unfinished User Stories

No Iteration 1 user story remained unfinished at closure.

| Category | Count | Estimated Work |
| --- | ---: | ---: |
| Completed stories | 3 | 7 days |
| Unfinished stories | 0 | 0 days |
| Partially completed stories | 0 | 0 days |

Features assigned to later iterations are not treated as unfinished Iteration 1 work because they were outside the agreed Iteration 1 scope.

## 5. Actual Velocity

Velocity is calculated using the original estimates of user stories that meet the team's completion conditions at the end of the iteration.

```text
Actual Velocity
= sum of estimates for completed Iteration 1 user stories
= 2 + 3 + 2
= 7 development days per iteration
```

| Measure | Result |
| --- | ---: |
| Planned Iteration 1 workload | 7 days |
| Completed workload | 7 days |
| Unfinished workload | 0 days |
| Actual velocity | **7 days/iteration** |
| Completion rate | **100%** |
| Story-level variance | **0 days** |

The planning value to carry into Iteration 2 is therefore **7 estimated development days**, subject to the scope and team availability of the next iteration.

## 6. Task-Level Estimate Reconciliation

The nine retrospective GitHub task issues contain estimates totalling five days, while the original three user stories total seven days.

| Estimation level | Total |
| --- | ---: |
| Original user-story estimates | 7 days |
| Estimates recorded in nine GitHub issues | 5 days |
| Difference | 2 days |

The difference exists because the GitHub issues were added retrospectively during Practical 4 and represent grouped tracking tasks rather than a complete replacement for the detailed task breakdown. Several activities included in the original story estimates are embedded within broader issues or are not represented as separate issues, including templates, URL configuration, login/logout configuration, form work and interface presentation.

For this iteration, velocity is calculated from the original user-story estimates because those estimates define the committed iteration scope. The five-day issue total must not be presented as a second velocity figure.

For future iterations, task issues should be created before implementation and their estimates should be back-checked so that the task total equals the related user-story estimate.

## 7. What Went Well

- The iteration delivered all three committed user stories.
- Django generic views and reusable forms kept the implementation small and maintainable.
- Owner-based filtering protected private data consistently.
- Automated tests covered authentication, CRUD operations and user isolation.
- The usability review produced a focused improvement rather than only a written observation.
- Pull request #10 provided evidence of review, validation and controlled merging.
- Week 4 documentation connected implementation, design diagrams, task tracking and version-control evidence.

## 8. What Could Be Improved

- Issues and estimates should be created before work starts rather than reconstructed afterwards.
- Task estimates should fully reconcile with their parent user-story estimates.
- Status changes should be recorded while work moves through `todo`, `in-progress` and `done`.
- Development should use smaller commits made when each unit of work is completed.
- Acceptance evidence should be linked to each user story as part of its definition of done.
- Future iterations should maintain a burndown record from the start rather than reconstructing progress at the end.

## 9. Actions for Iteration 2

1. Use **7 development days** as the initial capacity reference.
2. Select Iteration 2 user stories whose estimates fit within that capacity.
3. Create all task issues before implementation begins.
4. Ensure task estimates back-check against each parent story.
5. Assign owners and initial `todo` status immediately.
6. Move tasks through `in-progress` and `done` as work occurs.
7. Link commits, tests, review comments and demonstrations to completed stories.
8. Record remaining effort regularly so a defensible burndown graph can be produced.

## 10. Conclusion

Iteration 1 completed all committed scope and achieved an actual velocity of **7 estimated development days per iteration**. The implementation result was successful, while the largest process improvement is to make task tracking prospective and internally consistent during Iteration 2.
