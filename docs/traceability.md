# Feature Traceability

This matrix links every delivered capability to its implementation, automated
tests and acceptance evidence. Feature names are the stable identifiers; the
matrix does not depend on GitHub Issue or Pull Request numbering.

| Delivered capability | Iteration | Main implementation | Automated evidence | Completion evidence |
| --- | --- | --- | --- | --- |
| Secure account access | Foundation | `RegistrationForm`, `RegisterView`, `SafeLoginView`, authentication mixins | `books/tests.py` registration and authentication suites | [Account access](week5/user-stories/story-01-account-access.md) |
| Shared catalogue search and import | Foundation | `books/services.py`, `BookSearchView`, `BookImportView`, `CatalogBook` | `books/test_community.py` Open Library and import suites | [Catalogue import](week5/user-stories/story-02-catalogue-import.md) |
| Personal shelf and reading statuses | Foundation | `Book`, owner-scoped views, status endpoint, private notes | `books/tests.py`, `books/test_notes.py` | [Personal shelf](week5/user-stories/story-03-personal-shelf.md) |
| Category and trait discovery | Community | `Category`, catalogue browse, subject search and fallback | `books/test_discovery.py`, `books/test_community.py` | [Category discovery](week7/user-stories/story-04-category-discovery.md) |
| Public ratings and reviews | Community | `PublicReview`, review forms and permission views | `books/test_reviews.py` | [Ratings and reviews](week7/user-stories/story-05-public-reviews.md) |
| Custom lists and public profiles | Community | `ReadingList`, list views, community search and public profiles | `books/test_discovery.py`, `books/test_system.py` | [Lists and profiles](week7/user-stories/story-06-lists-profiles.md) |
| Forums and threaded replies | Delivery | `Forum`, `ForumPost`, `ForumReply` and permission views | `books/test_community.py` | [Forums and replies](week9/story-07-forums.md) |
| Personalised recommendations | Delivery | dashboard ranking, API fallback, `RecommendationDismissal` | `books/test_discovery.py` | [Recommendations](week9/story-08-recommendations.md) |
| Moderation and production delivery | Delivery | moderation centre, metadata/category controls, Render configuration | `books/test_community.py`, `books/test_system.py`, deployment checks | [Moderation and delivery](week9/story-09-moderation-delivery.md) |

## Version-control evidence

The repository's commit and Pull requests views preserve the chronological
implementation record. Current delivery claims are determined by the code and
tests on `main`; historical branch names or GitHub record numbers are not used
as feature identifiers.
