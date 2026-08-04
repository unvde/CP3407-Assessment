# Story 04 — Category and Trait Discovery

**Issue:** [#4](https://github.com/unvde/CP3407-Assessment/issues/4)

**Iteration:** 2 · **Estimate:** 3 development-days · **Status:** Done

## Delivered behaviour

- Community catalogue books use normalised, reusable categories.
- Readers can browse quick traits or search the wider Open Library Subjects API.
- Subject results support offsets and pagination.
- Aliases converge on canonical category names.
- A live API timeout falls back to local catalogue matches.

## Evidence

- Implementation: `Category`, catalogue list/detail views and subject search in `books/services.py`.
- Tests: `CategoryBrowseTests`, `CategoryModerationTests` and Open Library subject-service tests.
- Live proof: Explore books exposes trait search, quick categories, local catalogue results and review aggregates.
