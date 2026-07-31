# Practical 7 Report — Test-Driven Development

## Objective

Practical 7 requires the team to discuss, document and plan suitable project
testing, select at least five user stories, write at least three test cases for
each selected story, and implement at least 15 automated tests.

## Repository Baseline

The work began on the Iteration 2 development branch, now named
`iteration-2`. At the baseline, Reading Compass had one Django app, one model,
two forms, account views and owner-scoped book CRUD views.

The initial suite contained 18 tests. The baseline command passed:

```text
Found 18 test(s).
Ran 18 tests
OK
System check identified no issues (0 silenced).
```

## Testing Discussion and Decisions

The main risks are access to another reader's data, broken authentication and
invalid book or progress values. The suite focuses on:

- authentication and session state;
- owner-only list, detail, edit and delete access;
- input validation at both form and model boundaries;
- positive, negative and boundary values;
- persistence, redirects and important template output.

Most cases use Django model, form and request tests. A short browser check is
used for the main pages instead of maintaining a separate end-to-end suite.

The detailed strategy, environment, entry/exit criteria, exclusions and risks
are recorded in the [test plan](test-plan.md).

## Selected User Stories

Seven acceptance-level stories were selected from backlog Stories 01–06:

1. access an account;
2. view a private personal list;
3. add valid book information;
4. maintain owned books;
5. update reading progress;
6. view a personal reading dashboard;
7. manage an optional reading target.

Each selected workflow has at least three automated cases. The mapping is in
[test cases](test-cases.md).

## Automated Test Implementation

The suite grew from 18 to **30 tests**. During review, overlapping cases were
removed so that each remaining test checks a different rule or failure mode.
The final set covers:

- valid and invalid account access;
- anonymous and cross-user access attempts;
- book input, ownership, editing and deletion;
- progress calculation, missing totals and page bounds;
- dashboard authentication, filtering and owner isolation; and
- future, past, removable and cross-user reading targets.

Iteration 2 Stories 04–06 account for 11 of the 30 tests.

## Final Test Result

Command:

```bash
.venv/bin/python manage.py test -v 2
```

Result:

```text
Found 30 test(s).
Ran 30 tests
OK
System check identified no issues (0 silenced).
```

The command uses Django's temporary in-memory database, so it does not change
development data.

## Browser Acceptance Check

The signed-in workflow was also checked in a local browser. A reader with an
empty dashboard added a Currently Reading book with 200 total pages, current
page 80 and a future target date. The detail page and personal dashboard both
showed 40% progress and the formatted target date, and the browser reported no
console errors.

## Practical 7 Requirement Check

| Requirement | Result |
|---|---|
| Discuss, document and plan testing | Completed in test plan and this report |
| Select at least 5 user stories | 7 selected |
| At least 3 test cases per story | 3–7 cases per story |
| At least 15 documented cases | 30 documented |
| At least 15 automated tests | 30 automated tests |
| Run the complete suite | 30/30 passed |

## Reflection and Next Steps

The most useful tests were the permission and boundary cases because they found
problems that a normal form submission would not show. Iteration 3 work will
reuse the same pattern: write the acceptance case first, implement the smallest
change that passes it, then rerun the 30-test regression suite.
