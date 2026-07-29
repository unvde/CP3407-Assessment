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

Tasks use the labels `todo`, `in-progress` and `done`. Issues [#1](https://github.com/unvde/CP3407-Assessment/issues/1)–[#9](https://github.com/unvde/CP3407-Assessment/issues/9) were created as retrospective Iteration 1 task tracking. Their final repository state is:

- User Account Access: Done
- Personal Reading List: Done
- Reading Status Management: Done
- Iteration 1 usability and acceptance review: Done

All nine tasks are assigned, labelled `done`, and closed as completed. The detailed issue mapping is recorded in [Iteration 1 Task Tracking](task-tracking.md).

GitHub Issue state is the verified status record. GitHub Project Board field values could not be verified through the available repository connection, so this report does not claim that separate Project fields were updated.

## 5. Design Documentation

The application structure is documented using:

- [Class Diagram](class-diagram.md)
- [Add Book Sequence Diagram](sequence-diagram.md)

Both diagrams are complete Mermaid diagrams stored in the repository. The class diagram explains the relationships among the Django user, book model, forms and views. The sequence diagram illustrates authentication, validation, owner assignment and persistence during book creation.

## 6. Development Evidence

Iteration 1 provides:

- Account registration
- Login and logout
- Protected application routes
- Private book list
- Add, view, edit and delete book workflows
- Controlled reading statuses
- Owner-only record access
- Responsive templates
- Automated tests

At the time of the pull-request experiment, the Django system check and all 17 automated tests passed.

## 7. Version-Control Practice

Meaningful commits separate Iteration documentation, project initialisation, feature implementation, automated testing, setup documentation and the focused usability improvement. Historical dates were not changed to simulate daily activity.

## 8. Pull-Request Experiment and Review

The pull-request experiment was completed in [PR #10 — Improve Iteration 1 form guidance and usability](https://github.com/unvde/CP3407-Assessment/pull/10).

- Branch: `feature/iteration-1-usability-review`
- Reviewer: Yuhao Guo (`yoimiya571`)
- Review state: Commented
- Review outcome: no blocking code or usability defects were found; the implementation was accepted
- Validation recorded in the PR: Django system check passed, the complete automated test suite passed, and the Add Book form was reviewed in the browser
- Merge result: merged into `main` on 29 July 2026
- Merge commit: `9b2010f08d8117a97248e7e9e0d82731a11c83f6`

The review specifically confirmed that the four reading statuses are explained in user-friendly language, the shared form displays the guidance for both add and edit workflows, the guidance is defined in `BookForm`, and automated coverage checks the Add Book page. See [Yuhao Guo's recorded review](https://github.com/unvde/CP3407-Assessment/pull/10#pullrequestreview-4805185166).

## 9. Practical Completion Checklist

- [x] Split Iteration 1 user stories into tasks.
- [x] Estimate each task.
- [x] Back-check task totals against story estimates.
- [x] Use `todo`, `in-progress` and `done` tracking labels.
- [x] Create, assign, label and close GitHub issues #1–#9.
- [x] Develop and store a class diagram.
- [x] Develop and store a sequence diagram for a key operation.
- [x] Use meaningful commits for current code.
- [x] Complete and record Yuhao Guo's usability review.
- [x] Complete, review and merge PR #10.
- [ ] Verify and, if necessary, synchronize separate GitHub Project Board field values.

## 10. Remaining Action

Open the repository's GitHub Project while signed in and verify that Issues #1–#9 appear in the Done column/status. This is the only Week 4 tracking item not verified through the available repository connection.
