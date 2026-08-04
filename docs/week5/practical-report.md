# Practical 5 — Iteration 1 Reflection

## Completed versus unfinished

Stories #1–#3 are Done; no committed Iteration 1 work carries over. Stories #4–#9 remain planned for later iterations rather than being classified as unfinished Iteration 1 work.

## SRP and DRY

The review found clear responsibility boundaries among models, forms, services and views. Open Library behaviour is isolated in `books/services.py`; ownership and staff checks are reused through mixins; form fields use a shared include. Details are in [`srp-dry-review.md`](srp-dry-review.md).

## Velocity

Accepted original effort is 2 + 3 + 2 = **7 development-days**. Completion rate is 100% and carry-over is zero.

## Published completion evidence

- [Story 01 — Secure Account Access](user-stories/story-01-account-access.md)
- [Story 02 — Shared Catalogue Search and Import](user-stories/story-02-catalogue-import.md)
- [Story 03 — Personal Shelf and Reading Statuses](user-stories/story-03-personal-shelf.md)

The [Iteration 1 review](iteration-review.md) records the acceptance result and capacity decision.
