# Story Traceability

This matrix is the single source of truth linking requirements to implementation, automated tests and acceptance evidence.

| Story | Iteration | Main implementation | Automated evidence | Completion page |
| --- | ---: | --- | --- | --- |
| [#1 Secure Account Access](https://github.com/unvde/CP3407-Assessment/issues/1) | 1 | `RegistrationForm`, `RegisterView`, `SafeLoginView`, authentication mixins | `books/tests.py` — registration and authentication suites | [Story 01](week5/user-stories/story-01-account-access.md) |
| [#2 Shared Catalogue Search and Import](https://github.com/unvde/CP3407-Assessment/issues/2) | 1 | `books/services.py`, `BookSearchView`, `BookImportView`, `CatalogBook` | `books/test_community.py` — Open Library and import suites | [Story 02](week5/user-stories/story-02-catalogue-import.md) |
| [#3 Personal Shelf and Reading Statuses](https://github.com/unvde/CP3407-Assessment/issues/3) | 1 | `Book`, owner-scoped views, status endpoint, private notes | `books/tests.py`, `books/test_notes.py` | [Story 03](week5/user-stories/story-03-personal-shelf.md) |
| [#4 Category and Trait Discovery](https://github.com/unvde/CP3407-Assessment/issues/4) | 2 | `Category`, catalogue browse, subject search and fallback | `books/test_discovery.py`, `books/test_community.py` | [Story 04](week7/user-stories/story-04-category-discovery.md) |
| [#5 Public Ratings and Reviews](https://github.com/unvde/CP3407-Assessment/issues/5) | 2 | `PublicReview`, review forms and permission views | `books/test_reviews.py` | [Story 05](week7/user-stories/story-05-public-reviews.md) |
| [#6 Custom Lists and Public Profiles](https://github.com/unvde/CP3407-Assessment/issues/6) | 2 | `ReadingList`, list views, community search and public profiles | `books/test_discovery.py`, `books/test_system.py` | [Story 06](week7/user-stories/story-06-lists-profiles.md) |
| [#7 Forums and Threaded Replies](https://github.com/unvde/CP3407-Assessment/issues/7) | 3 | `Forum`, `ForumPost`, `ForumReply` and permission views | `books/test_community.py` | [Story 07](week9/story-07-forums.md) |
| [#8 Personalised Recommendations](https://github.com/unvde/CP3407-Assessment/issues/8) | 3 | dashboard ranking, API fallback, `RecommendationDismissal` | `books/test_discovery.py` | [Story 08](week9/story-08-recommendations.md) |
| [#9 Moderation and Production Delivery](https://github.com/unvde/CP3407-Assessment/issues/9) | 3 | moderation centre, metadata/category controls, Render configuration | `books/test_community.py`, `books/test_system.py`, deployment checks | [Story 09](week9/story-09-moderation-delivery.md) |

## Pull-request evidence

- [PR #10](https://github.com/unvde/CP3407-Assessment/pull/10): focused Iteration 1 usability review.
- [PR #30](https://github.com/unvde/CP3407-Assessment/pull/30): planning and documentation checkpoint.
- [PR #31](https://github.com/unvde/CP3407-Assessment/pull/31): tested application increment.
- [PR #48](https://github.com/unvde/CP3407-Assessment/pull/48): Iteration 3 planning checkpoint.
- [PR #49](https://github.com/unvde/CP3407-Assessment/pull/49): tested Iteration 3 increment.
- [PR #51](https://github.com/unvde/CP3407-Assessment/pull/51): community catalogue, forums and deployment foundation.

PRs preserve repository history. The completion claim for each current Story is determined by its code and tests on `main`, not by treating every historical PR title as a separate requirement.
