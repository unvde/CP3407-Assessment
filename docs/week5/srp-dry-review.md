# SRP and DRY Review

## SRP findings

| Area | Responsibility | Result |
| --- | --- | --- |
| Models | persist catalogue, shelf, review, list, recommendation and forum rules | Domain state remains outside HTTP handling |
| Forms | validate user-editable input | Ownership and staff privilege are not browser-selectable fields |
| `books/services.py` | communicate with and normalise Open Library | External API behaviour is isolated and mockable |
| Views | coordinate request workflows | Distinct classes handle distinct actions |
| Permission mixins | centralise owner, author and staff scoping | Private/public boundaries are reusable |
| Templates | present page state and actions | Business constraints remain server-side |

## DRY findings

- `templates/includes/form_fields.html` centralises labels, widgets, help text and errors.
- `OwnedBookQuerysetMixin`, `OwnedReadingListMixin`, forum permission mixins and `StaffRequiredMixin` avoid repeated access rules.
- Category normalisation and Open Library parsing each have one implementation path.
- Model choices provide the single source for reading-status values.

## Outcome

The final structure keeps external integration, validation, persistence, request coordination and presentation separable. The complete regression suite is the safety net for refactoring.
