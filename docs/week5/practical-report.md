# Practical 5 Report

## Iteration 1 — Reflection

## 1. Objective

Practical 5 closes Iteration 1 by reviewing code quality, reconciling task and
story status, documenting completed and unfinished work, documenting each
completed story and calculating actual velocity.

## 2. Team

- **Tianyang Zhang:** Lead Developer and Technical Lead
- **Yuhao Guo:** Project Coordinator and Requirements, Documentation and QA Lead

## 3. SRP and DRY Review

The Iteration 1 model, forms and class-based views have focused
responsibilities. Owner-only querying and reading-status definitions are
already shared rather than duplicated.

One material DRY issue was corrected: book, login and registration templates
repeated their form-field rendering loop. They now reuse
`templates/includes/form_fields.html`. Full findings and the rationale for
changes not made are recorded in the [SRP and DRY Review](srp-dry-review.md).

## 4. Completed Versus Unfinished Stories

All three Iteration 1 stories are `done`:

| No. | User Story | Estimate | Status |
| --- | --- | ---: |:---:|
| 01 | User Account Access | 2 days | done |
| 02 | Personal Reading List | 3 days | done |
| 03 | Reading Status Management | 2 days | done |

There is no unfinished Iteration 1 story. Stories 04–10 remain `todo` in their
planned Iterations 2 and 3; none is currently `in-progress`. See the
[Iteration 1 Review](iteration-review.md) and
[Task and Story Tracking](task-tracking.md).

## 5. Completed Story Documentation

GitHub Pages-ready Markdown documentation now exists for:

- [Story 01 — User Account Access](user-stories/story-01-account-access.md)
- [Story 02 — Personal Reading List](user-stories/story-02-reading-list.md)
- [Story 03 — Reading Status Management](user-stories/story-03-reading-status.md)

These are local repository pages. Publishing them remotely remains a manual
GitHub action.

## 6. Actual Velocity

Only original estimates for stories meeting the definition of Done are counted:

```text
2 days + 3 days + 2 days = 7 estimated development-days
```

Iteration 1 actual velocity is therefore **7 estimated development-days per
iteration**, also expressed as **3 completed stories per iteration**. Planned
effort was seven estimated days, so the completion rate is `7 / 7 × 100% =
100%` and carry-over is zero. This measures completed estimated scope, not
calendar time.

## 7. Documentation Consistency

The Week 5 folder follows the previous weekly structure:

- a practical report summarises the week's objective and evidence;
- detailed topics use separate linked Markdown pages;
- tables retain the existing user-story numbers, names and day estimates;
- relative links connect the report, evidence and README navigation;
- status terms are normalised to `todo`, `in-progress` and `done`;
- remote-only facts are explicitly separated from local evidence.

The stale Week 3 story progress record and Week 2 backlog status were reconciled
with the completed Iteration 1 evidence. Exact historical dates were not
invented, and the incomplete Week 3 burndown remains unchanged because daily
actual values are unavailable.

## 8. Practical Completion Checklist

- [x] Review classes and templates against SRP.
- [x] Review the implementation against DRY.
- [x] Record findings and make the necessary DRY correction.
- [x] Reconcile local task and story statuses.
- [x] Document completed versus unfinished Iteration 1 stories.
- [x] Add a Markdown page for every completed user story.
- [x] Calculate actual Iteration 1 velocity and show the formula.
- [x] Check consistency with Weeks 1–4.
- [x] Identify remote GitHub actions that remain manual.

## 9. Completion Status

All local Practical 5 work is complete. The team manually confirmed the remote
Issue and Project Board states on 29 July 2026, and the confirmed Project Board
URL is recorded in the Week 3 documentation. GitHub Pages is not currently
configured; enabling it would be a separate public-publishing decision.
