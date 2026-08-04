# Practical 8 — Iteration 3 and TDD

## Iteration 2 reflection

Stories #4–#6 were accepted for seven estimated development-days. The shared catalogue reduced duplication across discovery, reviews and lists, while explicit visibility rules prevented private-list leakage.

## Iteration 3 adjustment

The demonstrated capacity remains seven days:

| Story | Estimate | Status at planning |
| --- | ---: | --- |
| #7 Forums and Threaded Replies | 3 | Todo |
| #8 Personalised Recommendations | 2 | Todo |
| #9 Moderation and Production Delivery | 2 | Todo |

## TDD and mocks

- UI designs and Story criteria define public-read/authenticated-write actions.
- Forum tests cover anonymous, author, other-reader and staff roles.
- Recommendation tests mock Open Library results and failures.
- Deployment acceptance combines focused checks with complete system journeys.

See [Iteration 3 specifications](test-specifications.md) and [mock-object research](mock-object-research.md).
