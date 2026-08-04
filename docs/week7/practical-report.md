# Practical 7 — Test-Driven Development

## Result

The test plan selects Stories #1–#6 and defines eighteen representative automated cases, exceeding the requirement of five Stories, three cases per selected Story and fifteen automated tests.

## TDD approach

1. Express validation, permission and failure behaviour as a failing test.
2. Implement the smallest model/form/service/view change that passes it.
3. Refactor shared responsibilities into services, mixins and shared templates.
4. Run the focused suite followed by complete regression and migration checks.

## Evidence

- [`test-cases.md`](test-cases.md) maps representative cases to test classes.
- `books/tests.py` covers authentication, shelf and filtering.
- `books/test_community.py` covers API integration, imports and shared-data permissions.
- `books/test_reviews.py` covers public reviews.
- `books/test_discovery.py` covers lists, profiles, traits and recommendations.
- `books/test_notes.py` and `books/test_system.py` cover private data and cross-feature journeys.

Iteration 2 Stories #4–#6 meet their acceptance criteria and their completion pages are linked from [`user-stories/README.md`](user-stories/README.md).
