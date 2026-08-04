# Story 05 — Public Ratings and Reviews

**Issue:** [#5](https://github.com/unvde/CP3407-Assessment/issues/5)

**Iteration:** 2 · **Estimate:** 2 development-days · **Status:** Done

## Delivered behaviour

- Ratings are integers from 1 to 5 and review content cannot be blank.
- A reader can maintain at most one review per catalogue book.
- Review text, author, date and aggregate rating are public.
- Authors can update their review; staff can remove public reviews.
- Anonymous visitors can read but are redirected from write routes.

## Evidence

- Implementation: `PublicReview`, `PublicReviewForm` and review permission views.
- Tests: six focused scenarios in `books/test_reviews.py`.
- Live proof: catalogue detail pages show aggregate ratings, individual public reviews and the Rate & review action.
