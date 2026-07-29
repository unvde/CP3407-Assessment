# Iteration 1 Task Tracking

## 1. Tracking Workflow

Iteration work is tracked using three statuses:

- **Todo:** The task is planned but has not started.
- **In Progress:** Implementation, testing or review is underway.
- **Done:** The task meets its acceptance conditions and has supporting evidence.

The issues were added retrospectively during Practical 4 to document the Iteration 1 task breakdown. They are not presented as real-time historical tracking.

## 2. Final Story Status

| No. | User Story | Owner | Estimate | Status | Evidence |
| --- | --- | --- | ---: | --- | --- |
| 01 | User Account Access | Tianyang Zhang | 2 days | Done | Registration, login, logout, protected pages and automated tests |
| 02 | Personal Reading List | Tianyang Zhang | 3 days | Done | Book CRUD workflow, owner isolation and automated tests |
| 03 | Reading Status Management | Tianyang Zhang and Yuhao Guo | 2 days | Done | Implementation and tests complete; usability review accepted in PR #10 |

## 3. GitHub Issue Record

| Issue | Task | Assignee | Label | State |
| --- | --- | --- | --- | --- |
| [#1](https://github.com/unvde/CP3407-Assessment/issues/1) | Configure account authentication workflow | `unvde` | `done` | Closed — completed |
| [#2](https://github.com/unvde/CP3407-Assessment/issues/2) | Implement registration and email validation | `unvde` | `done` | Closed — completed |
| [#3](https://github.com/unvde/CP3407-Assessment/issues/3) | Test authentication and protected routes | `unvde` | `done` | Closed — completed |
| [#4](https://github.com/unvde/CP3407-Assessment/issues/4) | Create Book model and migration | `unvde` | `done` | Closed — completed |
| [#5](https://github.com/unvde/CP3407-Assessment/issues/5) | Implement personal book CRUD workflow | `unvde` | `done` | Closed — completed |
| [#6](https://github.com/unvde/CP3407-Assessment/issues/6) | Enforce owner-only book access | `unvde` | `done` | Closed — completed |
| [#7](https://github.com/unvde/CP3407-Assessment/issues/7) | Test book management and user isolation | `unvde` | `done` | Closed — completed |
| [#8](https://github.com/unvde/CP3407-Assessment/issues/8) | Implement controlled reading statuses | `unvde` | `done` | Closed — completed |
| [#9](https://github.com/unvde/CP3407-Assessment/issues/9) | Perform Iteration 1 usability and acceptance review | `yoimiya571` (Yuhao Guo) | `done` | Closed — completed |

Issue #2 was corrected so its task description covers registration and unique-email validation rather than duplicating Issue #3's authentication-test task.

The repository labels use exactly `todo`, `in-progress` and `done`. All final Iteration 1 task issues use `done`.

## 4. Commit Evidence

| Commit | Purpose |
| --- | --- |
| `71ae7d0` | Initialise the Django project |
| `ce730a3` | Implement Iteration 1 reading management |
| `f0e1fdc` | Add Iteration 1 automated coverage |
| `7467500` | Add local setup and Week 3 navigation |
| `bc93f18` | Implement the focused Iteration 1 usability improvement |
| `9b2010f` | Merge PR #10 into `main` |

Historical dates were not changed or fabricated.

## 5. Pull Request and Review Evidence

[PR #10 — Improve Iteration 1 form guidance and usability](https://github.com/unvde/CP3407-Assessment/pull/10) completed the planned pull-request experiment.

- Reviewer: Yuhao Guo (`yoimiya571`)
- Recorded review: [COMMENTED review](https://github.com/unvde/CP3407-Assessment/pull/10#pullrequestreview-4805185166)
- Result: no blocking code or usability defects; implementation accepted
- Merge: completed into `main` on 29 July 2026

The review content is referenced from the existing GitHub review and is not reconstructed or invented in this document.

## 6. Project Board Status

The Issue assignees, labels and open/closed states above were verified and
synchronized. On 29 July 2026, the team also manually confirmed in a signed-in
GitHub session that Issues #1–#9 are present in the Project with Status = Done.
The Project Board URL is recorded in the Week 3 project-board document.

## 7. Completion Checklist

- [x] Create Issues #1–#9.
- [x] Assign each issue to the responsible team member.
- [x] Apply final `done` labels.
- [x] Correct Issue #2's task description.
- [x] Record Yuhao Guo's usability review without inventing content.
- [x] Complete and merge PR #10.
- [x] Close completed Issues #1–#9.
- [x] Add issue, review and pull-request links to Week 4 documentation.
- [x] Verify separate GitHub Project Board fields while signed in.
