# Requirements Backlog

## Priority Scale

- **10 - Essential:** Required for the minimum usable product
- **20 - High:** Important to the principal user workflow
- **30 - Medium:** Provides significant usability or planning value
- **40 - Low:** Valuable but not required for the initial release
- **50 - Optional:** Implemented only if time and budget permit

## 01 - User Account Access

**Description:** Allow users to register, sign in and sign out securely.

**User Story:** As a new reader, I want to create and access a personal account so that my reading information can be securely saved.

**Priority:** 10  
**Estimated Effort:** 2 days

**Rationale:** A personal account is required to associate private reading information with the correct user.

## 02 - Personal Reading List

**Description:** Allow users to add, view, edit and remove books in a personal reading list.

**User Story:** As a reader, I want to maintain a personal reading list so that I can keep books that interest me in one organised location.

**Priority:** 10  
**Estimated Effort:** 3 days

**Rationale:** The reading list is the central feature on which the remaining requirements depend.

## 03 - Reading Status Management

**Description:** Allow each book to be assigned a status such as Want to Read, Currently Reading, Paused or Completed.

**User Story:** As a reader, I want to assign a status to each book so that I can understand its position in my reading workflow.

**Priority:** 10  
**Estimated Effort:** 2 days

**Rationale:** Status information is necessary for organising books and displaying relevant dashboard information.

## 04 - Reading Progress Updates

**Description:** Allow users to record their current page and view calculated reading progress.

**User Story:** As a reader, I want to update my current reading position so that I can see how much of a book I have completed.

**Priority:** 10  
**Estimated Effort:** 3 days

**Rationale:** Progress tracking directly addresses the main purpose of the application.

## 05 - Reading Dashboard

**Description:** Display active books, current progress and upcoming reading targets in one summary.

**User Story:** As a reader, I want to view a personal dashboard so that I can quickly understand my current reading activity.

**Priority:** 20  
**Original Estimated Effort:** 3 days

**Iteration 2 Adjusted Effort:** 2 days

**Rationale:** The dashboard improves access to information produced by the core features.

## 06 - Reading Plans

**Description:** Allow users to set an optional target completion date for a book.

**User Story:** As a reader, I want to set an optional completion target so that I can plan my reading without being forced to schedule every book.

**Priority:** 20  
**Estimated Effort:** 2 days

**Rationale:** Planning supports consistent reading while remaining flexible for casual users.

## 07 - Search and Filtering

**Description:** Allow users to search by title or author and filter books by reading status.

**User Story:** As a reader, I want to search and filter my reading list so that I can quickly locate relevant books.

**Priority:** 30  
**Estimated Effort:** 2 days

**Rationale:** Search and filtering become more valuable as the number of saved books increases.

## 08 - Private Reading Notes

**Description:** Allow users to create, edit and delete private notes associated with a book.

**User Story:** As a reader, I want to save private notes for a book so that I can retain important ideas and observations.

**Priority:** 30  
**Estimated Effort:** 3 days

**Rationale:** Notes support reflection but are not required for basic reading-list and progress management.

## 09 - Completion Review

**Description:** Allow users to save a rating, completion date and short reflection after finishing a book.

**User Story:** As a reader, I want to review a completed book so that I can preserve my opinion and learning.

**Priority:** 40  
**Estimated Effort:** 2 days

**Rationale:** Completion reviews add long-term value but depend on the core book and status features.

## 10 - Duplicate Book Warning

**Description:** Warn users when they attempt to add a book with the same title and author as an existing entry.

**User Story:** As a reader, I want to be warned about possible duplicate books so that my reading list remains organised.

**Priority:** 50  
**Estimated Effort:** 1 day

**Rationale:** Duplicate prevention improves data quality but is not essential to the primary workflow.

## Effort Summary

| Priority | Requirements | Estimated Effort |
|:---:|---:|---:|
| 10 | 4 | 10 days |
| 20 | 2 | 5 days |
| 30 | 2 | 5 days |
| 40 | 1 | 2 days |
| 50 | 1 | 1 day |
| **Total** | **10** | **23 days** |

## Current Story Status

Status uses the shared workflow `todo`, `in-progress` and `done`.

| No. | User Story | Iteration | Status |
|:---:|---|:---:|:---:|
| 01 | User Account Access | 1 | done |
| 02 | Personal Reading List | 1 | done |
| 03 | Reading Status Management | 1 | done |
| 04 | Reading Progress Updates | 2 | in-progress |
| 05 | Reading Dashboard | 2 | todo |
| 06 | Reading Plans | 2 | todo |
| 07 | Search and Filtering | 3 | todo |
| 08 | Private Reading Notes | 3 | todo |
| 09 | Completion Review | 3 | todo |
| 10 | Duplicate Book Warning | 3 | todo |

Iteration 1 is closed. Iteration 2 started in Week 6, and Story 04 is
`in-progress` at the Week 6 planning checkpoint. Detailed Iteration 1
evidence and velocity are recorded in the
[Week 5 Iteration Review](../week5/iteration-review.md).

The Iteration 2 plan was adjusted in Week 6 to match the demonstrated velocity
of 7 estimated development-days. Story 05 was narrowed from 3 to 2 days; its
first release is limited to active books, progress and optional target dates.
The detailed scope and rationale are recorded in the
[Week 6 Practical Report](../week6/practical-report.md).

## Planning Conclusion

The four priority-10 requirements form the minimum usable product. Priority-20 requirements should follow once the core reading workflow is stable. Priority-30 to priority-50 requirements may be scheduled according to the team's demonstrated velocity and remaining project budget.
