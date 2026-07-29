# Practical 4 Report

## Iteration 1 — Execution and Tracking

## 1. Objective

The objective of Practical 4 is to continue Iteration 1 development and improve the way work is decomposed, estimated, tracked, reviewed and documented.

## 2. Team

- **Tianyang Zhang:** Lead Developer and Technical Lead
- **Yuhao Guo:** Project Coordinator and Requirements, Documentation and QA Lead

## 3. Task Decomposition and Estimation

The three Iteration 1 user stories were split into implementation, testing and review tasks.

| User Story | Original Estimate | Task Estimate | Variance |
| --- | ---: | ---: | ---: |
| User Account Access | 2 days | 2 days | 0 |
| Personal Reading List | 3 days | 3 days | 0 |
| Reading Status Management | 2 days | 2 days | 0 |
| **Total** | **7 days** | **7 days** | **0 days** |

The detailed breakdown is available in [Iteration 1 Task Breakdown](task-breakdown.md).

## 4. Progress Tracking

Tasks use the labels `todo`, `in-progress` and `done`.

Current implementation evidence shows:

- User Account Access: Done
- Personal Reading List: Done
- Reading Status Management: implementation and automated testing done; team usability review in progress

The tracking plan, issue structure and commit evidence are documented in [Iteration 1 Task Tracking](task-tracking.md).

## 5. Design Documentation

The current application structure is documented using:

- [Class Diagram](class-diagram.md)
- [Add Book Sequence Diagram](sequence-diagram.md)

The class diagram explains the relationships among the Django user, book model, forms and views. The sequence diagram illustrates authentication, validation, owner assignment and persistence during book creation.

## 6. Development Evidence

Iteration 1 currently provides:

- Account registration
- Login and logout
- Protected application routes
- Private book list
- Add, view, edit and delete book workflows
- Controlled reading statuses
- Owner-only record access
- Responsive templates
- Automated tests

The Django system check passes, and all 17 automated tests pass.

## 7. Version-Control Practice

Meaningful commits separate:

- Iteration documentation
- Project initialisation
- Feature implementation
- Automated testing
- Setup documentation

Future work should be committed on the days it is performed using focused commit messages. Historical dates must not be changed to simulate daily activity.

## 8. Pull-Request Experiment

The team will use a focused usability improvement to practise the pull-request workflow:

1. Create `feature/iteration-1-usability-review`.
2. Make and test one focused improvement.
3. Push the branch.
4. Open a pull request into `main`.
5. Request review from Yuhao Guo when repository permissions allow.
6. Respond to feedback before merging.

The pull-request URL and review outcome must be added after the experiment is completed.

## 9. Practical Completion Checklist

- [x] Split Iteration 1 user stories into tasks.
- [x] Estimate each task.
- [x] Back-check task totals against story estimates.
- [x] Define `todo`, `in-progress` and `done` tracking labels.
- [x] Develop a class diagram.
- [x] Develop a sequence diagram for a key operation.
- [x] Use meaningful commits for current code.
- [ ] Create or update GitHub issues and assignments.
- [ ] Record actual GitHub Project statuses.
- [ ] Complete Yuhao Guo's usability review.
- [ ] Experiment with a pull request and record its review.
- [ ] Add external diagram links or exports if required.

## 10. Next Steps

1. Create the planned GitHub issues.
2. Assign implementation and review responsibilities.
3. Complete the usability review.
4. Conduct the pull-request experiment.
5. Update the task and Practical reports with actual links and outcomes.
6. Continue recording real progress for the Iteration 1 burndown.

