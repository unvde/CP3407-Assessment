# Iteration 3 Final Acceptance

## Week 9 Day 6

Iteration 3 closes with integrated system testing, defect review, full
regression and documentation reconciliation. The accepted scope is Story 07
Search and Filtering, Story 08 Private Reading Notes and Story 09 Completion
Review. Story 10 remains outside the selected capacity and was not started.

## System Test Plan and Results

| ID | Integrated scenario | Expected result | Result |
|---|---|---|:---:|
| SYS-01 | Create a book, find it by search/status, complete it, add a private note and add a completion review | The same owned record moves through every Iteration 3 workflow and displays its private data | Pass |
| SYS-02 | Request another reader's matching book, note mutations and review workflow | Search returns no record; detail and every mutation return 404; private data remains unchanged | Pass |
| SYS-03 | Anonymous reader requests note create/edit/delete and completion-review routes | Every write route redirects to sign in with the requested destination retained | Pass |

All three system tests pass and are implemented in
`books.test_system.IterationThreeSystemTests`.

## Defect Log

| ID | Finding | Disposition | Status |
|---|---|---|:---:|
| DEF-01 | Story 09 detail test text matched an existing Story 08 heading and produced a false positive | Replaced it with unique review content and confirmed the pre-display red state | Closed |
| DEF-02 | `TextField(max_length=1000)` did not enforce the boundary during model `full_clean()` | Added explicit `MaxLengthValidator(1000)` and passed the 1000/1001 boundary test | Closed |
| DEF-03 | Workflow spy expected one course-day lookup while form and model validation correctly performed two | Corrected the test to verify both validation layers | Closed |
| DEF-04 | Local development database had unapplied Iteration 3 migrations | Reviewed the plan, applied migrations 0004 and 0005, and passed `migrate --check` | Closed |

No open functional, privacy, validation or migration defects remain.

## Final Verification

- Iteration 3 system tests: 3 passed;
- complete Django regression: 68 passed;
- Django system check: no issues;
- migration drift: no changes detected;
- local migration application check: passed;
- owner isolation: verified across search, notes and completion reviews;
- Story and task Issues: all 16 committed items closed with `done`;
- Story 10: not started; and
- draft PR: reconciled for ready-for-review transition after this record is
  published.

## Acceptance Decision

Stories 07–09 meet their acceptance criteria and the Iteration 3 Definition of
Done. The completed effort is 7 development-days, matching the selected
capacity. Iteration 3 is accepted and ready for review.
