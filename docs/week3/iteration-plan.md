# Three-Iteration Plan

## Capacity

The milestone uses three iterations with a seven-development-day planning capacity in each iteration. Story order is driven by dependency and risk rather than by page count.

## Iteration 1 — Secure reading foundation

| Story | Estimate | Dependency rationale |
| --- | ---: | --- |
| #1 Secure Account Access | 2 days | Identity and permission boundaries protect every private workflow. |
| #2 Shared Catalogue Search and Import | 3 days | A canonical catalogue prevents duplicate metadata before community features are added. |
| #3 Personal Shelf and Reading Statuses | 2 days | The private shelf links a reader to the shared catalogue. |
| **Total** | **7 days** | |

Increment: a reader can create an account, find or import a book, add it to a private shelf and manage its status without exposing personal data.

## Iteration 2 — Discovery and curation

| Story | Estimate | Dependency rationale |
| --- | ---: | --- |
| #4 Category and Trait Discovery | 3 days | Builds on the shared catalogue and adds local/API discovery. |
| #5 Public Ratings and Reviews | 2 days | Adds controlled public contributions to catalogue books. |
| #6 Custom Lists and Public Profiles | 2 days | Reuses catalogue books and reviews while enforcing explicit privacy. |
| **Total** | **7 days** | |

Increment: readers can discover books by traits, publish opinions and curate public or private collections.

## Iteration 3 — Community and delivery

| Story | Estimate | Dependency rationale |
| --- | ---: | --- |
| #7 Forums and Threaded Replies | 3 days | Adds the most complex author/staff permission matrix. |
| #8 Personalised Recommendations | 2 days | Uses accumulated shelf and category information. |
| #9 Moderation and Production Delivery | 2 days | Completes staff controls, deployment and system acceptance. |
| **Total** | **7 days** | |

Increment: readers can hold contextual discussions and receive recommendations; staff can moderate public content; the application is deployed and acceptance-tested.

## Definition of Done

A Story is Done only when its acceptance criteria pass, owner/staff boundaries are tested, the complete regression suite remains green, documentation links to real code and tests, and its canonical Issue records the result.
