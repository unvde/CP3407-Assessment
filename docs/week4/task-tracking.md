# Iteration 1 Task Tracking

## 1. Tracking Workflow

Iteration work is tracked using three statuses:

- **Todo:** The task is planned but has not started.
- **In Progress:** Implementation, testing or review is underway.
- **Done:** The task meets its acceptance conditions and has supporting evidence.

## 2. Current Story Status

| No. | User Story | Owner | Estimate | Status | Evidence |
| --- | --- | --- | ---: | --- | --- |
| 01 | User Account Access | Tianyang Zhang | 2 days | Done | Registration, login, logout, protected pages and automated tests |
| 02 | Personal Reading List | Tianyang Zhang | 3 days | Done | Book CRUD workflow, owner isolation and automated tests |
| 03 | Reading Status Management | Tianyang Zhang | 2 days | In Progress | Implementation and tests complete; team usability review pending |

## 3. GitHub Issue Plan

The following issues should be created and assigned on the Iteration 1 GitHub Project:

| Suggested Issue Title | Story | Assignee | Initial Label |
| --- | --- | --- | --- |
| Configure account authentication workflow | 01 | Tianyang Zhang | done |
| Implement registration and email validation | 01 | Tianyang Zhang | done |
| Test authentication and protected routes | 01 | Tianyang Zhang | done |
| Create Book model and migration | 02 | Tianyang Zhang | done |
| Implement personal book CRUD workflow | 02 | Tianyang Zhang | done |
| Enforce owner-only book access | 02 | Tianyang Zhang | done |
| Test book management and user isolation | 02 | Tianyang Zhang | done |
| Implement controlled reading statuses | 03 | Tianyang Zhang | done |
| Perform Iteration 1 usability and acceptance review | 03 | Yuhao Guo | in-progress |

The issue labels should use exactly:

- `todo`
- `in-progress`
- `done`

Issue statuses must reflect actual work. Creating issues after implementation should be documented as retrospective task tracking rather than presented as real-time tracking.

## 4. Commit Evidence

The current Iteration 1 implementation is represented by meaningful commits:

| Commit | Purpose |
| --- | --- |
| `71ae7d0` | Initialise the Django project |
| `ce730a3` | Implement Iteration 1 reading management |
| `f0e1fdc` | Add Iteration 1 automated coverage |
| `7467500` | Add local setup and Week 3 navigation |

Future development should use smaller daily commits when work occurs on separate days. Commit dates must not be changed or fabricated.

## 5. Pull Request Experiment

A pull request should be used for the next reviewable change:

1. Create a feature branch from `main`.
2. Make one focused improvement.
3. Push the feature branch.
4. Open a pull request targeting `main`.
5. Assign Yuhao Guo as reviewer when repository access permits.
6. Record review comments and any resulting changes.
7. Merge only after tests pass and review is complete.

Suggested experiment:

```text
Branch: feature/iteration-1-usability-review
PR title: Improve Iteration 1 form guidance and usability
Reviewer: Yuhao Guo
```

## 6. Remaining Tracking Actions

- [ ] Create or update the Iteration 1 GitHub Project.
- [ ] Create the planned issues.
- [ ] Assign each issue to the responsible team member.
- [ ] Apply `todo`, `in-progress` and `done` labels.
- [ ] Record Yuhao Guo's usability review.
- [ ] Conduct the pull-request experiment.
- [ ] Add the Project and pull-request links to this document.

