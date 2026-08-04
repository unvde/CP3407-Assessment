# Week 7 Automated Test Cases

Practical 7 requires at least five selected Stories and at least three cases per Story. The following matrix uses six Stories and eighteen representative automated cases; the repository contains additional tests.

| ID | Story | Scenario | Expected result | Automated location |
| --- | --- | --- | --- | --- |
| TC-01 | #1 | Register with valid email and passwords | Account created and user signed in | `RegistrationTests` |
| TC-02 | #1 | Register with duplicate email | Validation rejects duplicate | `RegistrationTests` |
| TC-03 | #1 | Ordinary reader follows staff `next` URL | Redirect remains safe | `AuthenticationTests` |
| TC-04 | #2 | Search Open Library | Normalised results displayed | `OpenLibraryServiceTests` |
| TC-05 | #2 | Import a valid signed result twice | Catalogue and shelf records reused | `BookImportTests` |
| TC-06 | #2 | Submit tampered token | Request rejected | `BookImportTests` |
| TC-07 | #3 | View personal shelf | Only owner's books displayed | `BookManagementTests` |
| TC-08 | #3 | Change status | Valid controlled status persists | `BookManagementTests` |
| TC-09 | #3 | Access another reader's book/note | 404 without disclosure | book and note suites |
| TC-10 | #4 | Search a trait | Subject results and paging displayed | `CategoryBrowseTests` |
| TC-11 | #4 | Resolve a category alias | Canonical category reused | `CategoryModerationTests` |
| TC-12 | #4 | Subject API times out | Local category results remain usable | `CategoryBrowseTests` |
| TC-13 | #5 | Submit rating outside 1–5 | Validation rejects it | `PublicReviewTests` |
| TC-14 | #5 | Create a second review for same book | Uniqueness prevents duplication | `PublicReviewTests` |
| TC-15 | #5 | Read catalogue detail anonymously | Review and aggregate are public | `PublicReviewTests` |
| TC-16 | #6 | Owner adds/removes a list book | List membership changes | `ReadingListTests` |
| TC-17 | #6 | Another reader edits the list | Mutation rejected | `ReadingListTests` |
| TC-18 | #6 | View community search/profile | Private lists are absent | `PublicDiscoveryTests` |

All tests use isolated Django test data. External Open Library interactions are mocked.
