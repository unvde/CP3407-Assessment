# Iteration 3 Final Acceptance

## Accepted scope

| Story | Estimate | Result | Evidence |
| --- | ---: | --- | --- |
| #7 Forums and Threaded Replies | 3 days | Done | forum and reply permission suites |
| #8 Personalised Recommendations | 2 days | Done | local ranking, external fallback and dismissal tests |
| #9 Moderation and Production Delivery | 2 days | Done | moderation, category, deployment and system checks |
| **Total** | **7 days** | **100%** | |

Actual velocity is **7 development-days** with no carry-over.

## System journeys

| Journey | Expected result | Result |
| --- | --- | --- |
| Reader imports a book, changes status, reviews it and adds it to a list | Each step persists and remains associated with the authenticated reader | Pass |
| Reader attempts to mutate another reader's shelf or private list | Request is rejected without data disclosure | Pass |
| Anonymous visitor requests public write routes | Redirect to login while public read pages remain available | Pass |
| Staff opens moderation and manages shared content | Staff succeeds; ordinary reader is rejected | Pass |

## Final decision

All nine planned Stories are represented in the deployed application and linked to focused automated tests. The complete regression, Django checks, migration checks and delivery configuration form the release gate. The final demonstration follows [`final-demo-checklist.md`](final-demo-checklist.md).
