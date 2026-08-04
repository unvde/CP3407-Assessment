# Story 08 — Personalised Recommendations

**Issue:** [#8](https://github.com/unvde/CP3407-Assessment/issues/8)

**Iteration:** 3 · **Estimate:** 2 development-days · **Status:** Done

## Delivered behaviour

- Dashboard recommendations rank catalogue books that share the reader's categories.
- Books already owned by the reader are excluded.
- External Open Library results fill sparse local recommendations.
- Not interested creates a persistent dismissal and removes that suggestion.
- External failure leaves local recommendations or a usable empty state.

## Evidence

- Implementation: recommendation ranking in `DashboardView`, `RecommendationDismissal` and dismiss endpoint.
- Tests: `RecommendationTests` in `books/test_discovery.py` with mocked external search.
- Live proof: Dashboard shows reason text such as shared categories and a Not interested action for every suggestion.
