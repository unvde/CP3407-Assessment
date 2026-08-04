# Target-User Interview Findings

## Method

The team used semi-structured conversations with student and casual readers to understand discovery, tracking, sharing and privacy needs. Findings were consolidated rather than attributing personal comments to named participants.

## Main problems

- Re-entering book title, author and publication data is tedious.
- Private reading state and notes should not become public accidentally.
- Genre labels are inconsistent across sources.
- Reviews are useful only when rating and authorship rules are clear.
- Readers want collections that may be shared selectively.
- General social feeds lose the context of the book being discussed.
- Recommendations become repetitive without a dismissal mechanism.

## Requirements derived from feedback

| Finding | Product response |
| --- | --- |
| Reduce repeated entry | Open Library search and shared catalogue import |
| Protect personal activity | owner-scoped shelf, statuses and private notes |
| Improve discovery | normalised categories, trait search and recommendations |
| Support useful sharing | ratings/reviews, public/private lists and profiles |
| Keep discussion contextual | one forum per catalogue book with threaded replies |
| Protect the community | staff moderation, metadata maintenance and deployment checks |

## Usability expectations

Readers preferred direct navigation, one clear search field, human-readable status labels, visible privacy state, obvious empty states and usable mobile layouts. These expectations informed the implemented My books, Dashboard, Find a book, Explore, Lists, Profiles and Forum screens.

## Privacy expectations

Private shelf records and notes must be owner-scoped; private lists must not appear in community search or profiles; anonymous users may read public content but must authenticate before writing; staff privileges must be explicit and tested.

The resulting formal backlog is recorded in [`requirements-backlog.md`](requirements-backlog.md).
