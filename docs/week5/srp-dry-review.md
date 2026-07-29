# SRP and DRY Review

## 1. Purpose

This review checks the Iteration 1 implementation against the Single
Responsibility Principle (SRP) and Don't Repeat Yourself (DRY). The scope covers
the `Book` model, forms, views, URL configuration, templates and tests.

## 2. SRP Findings

| Area | Finding | Result |
| --- | --- | --- |
| `Book` model | Stores book data, reading-status choices and model-level navigation. It does not handle requests or presentation. | Satisfies SRP for the current scope |
| `RegistrationForm` | Owns registration input and unique-email validation. | Satisfies SRP |
| `BookForm` | Owns editable book fields and input normalisation. | Satisfies SRP |
| `RegisterView` | Coordinates account creation and signs in the newly created user. | Focused view responsibility |
| Book class-based views | List, detail, create, update and delete workflows are separate classes. | Satisfies SRP |
| `OwnedBookQuerysetMixin` | Centralises the single concern of owner-scoped querying and authentication. | Satisfies SRP and supports reuse |
| Templates | Presentation remains outside models, forms and views. | Satisfies SRP |

No class currently has a clear second reason to change that warrants further
splitting. In particular, adding a service layer for the small create and
registration workflows would add complexity without separating a meaningful
domain responsibility.

## 3. DRY Findings and Corrections

### Corrected: repeated form-field rendering

The book, login and registration templates repeated the same loop for labels,
widgets, help text and validation errors. This created three places that would
need to change for a presentation or accessibility correction.

The repeated markup was moved to
`templates/includes/form_fields.html`. All three forms now include that shared
partial. Their page-specific headings, buttons and redirect fields remain in
their own templates.

### Already DRY: owner-only access

List, detail, update and delete views reuse `OwnedBookQuerysetMixin` rather than
duplicating authenticated owner filters. Create keeps its distinct
responsibility: assigning the current user as owner before saving.

### Already DRY: reading-status definitions

The four allowed values and user-facing labels are defined once in
`Book.ReadingStatus`. Forms and templates consume the model choices and display
labels rather than maintaining independent status lists.

### Acceptable repetition: test setup and page wording

Some test data creation is repeated across test classes, but each class has a
different fixture scope and the repetition is small and explicit. Page-specific
headings and actions are intentional content, not duplicated business rules.

## 4. Outcome

The Iteration 1 classes have focused responsibilities. One material template
duplication was removed. No behavioural or database change was required, and
the existing automated suite is used to verify that the refactor preserves the
completed user stories.
