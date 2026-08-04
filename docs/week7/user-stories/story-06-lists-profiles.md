# Story 06 — Custom Lists and Public Profiles

**Issue:** [#6](https://github.com/unvde/CP3407-Assessment/issues/6)

**Iteration:** 2 · **Estimate:** 2 development-days · **Status:** Done

## Delivered behaviour

- Readers create public or private named lists and add/remove catalogue books.
- Only the owner may edit or delete a list.
- Community search matches list, reader, book, author and category information.
- Private lists are excluded from community discovery and public profiles.
- Public profiles combine intentionally public lists and recent reviews.

## Evidence

- Implementation: `ReadingList`, list CRUD, community-list search and `UserPublicProfileView`.
- Tests: `ReadingListTests`, `PublicDiscoveryTests` and system owner-boundary coverage.
- Live proof: My lists, Community lists and reader profile pages expose the complete workflow.
