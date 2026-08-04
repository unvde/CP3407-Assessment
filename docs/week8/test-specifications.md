# Iteration 3 TDD Specifications

## Story 07 — Forums and Threaded Replies

1. A catalogue book cannot have two forums.
2. Anonymous visitors can read but are redirected from forum writes.
3. A post author can edit their post; another reader cannot.
4. A reply author can edit their reply; another reader cannot.
5. Staff can delete any forum, post or reply.

## Story 08 — Personalised Recommendations

1. Matching-category books rank ahead of unrelated books.
2. Books already on the reader's shelf are excluded.
3. A dismissal persists and hides the suggestion.
4. Mocked external results fill a sparse local set.
5. External failure leaves a usable local or empty result.

## Story 09 — Moderation and Production Delivery

1. Moderation routes reject anonymous and ordinary users.
2. Staff can see and remove public contributions.
3. Category aliases are normalised; staff can rename/delete categories.
4. Staff can refresh catalogue metadata while ordinary readers cannot.
5. Demo seeding is idempotent.
6. Integrated reader, owner-boundary and anonymous-write journeys pass.

## Exit criteria

- Focused suites pass.
- Complete Django regression passes.
- System check and migration-drift check pass.
- Deployment configuration and health route are present.
