# Week 7 Test Plan

## Scope

Testing covers Stories #1–#6 and protects the foundation needed by Iteration 3: authentication, catalogue import, private shelf/statuses, category discovery, public reviews, lists and profiles.

## Test levels

- Model and form tests for constraints, validation and normalisation.
- View tests for successful workflows, authentication and ownership.
- Service tests with mocked Open Library responses and failures.
- Acceptance tests for public/private visibility and author/staff permissions.
- System journeys that cross multiple features.

## Entry criteria

- Acceptance criteria are written before implementation.
- Test data identifies owner, other reader, anonymous visitor and staff roles.
- External calls have deterministic mocks.

## Exit criteria

- At least three cases are implemented for each selected Story.
- At least fifteen automated tests pass.
- Complete regression passes with no migration drift.
- Failed permission checks do not disclose private objects.

## Risks and controls

| Risk | Control |
| --- | --- |
| Live API instability | Mock success, timeout and sparse-result behaviour |
| Cross-reader data leak | Repeat owner/other-reader checks on every private model |
| Public/private list confusion | Search and profile tests explicitly exclude private lists |
| Staff privilege leakage | Anonymous, reader and staff cases for moderation-adjacent actions |
