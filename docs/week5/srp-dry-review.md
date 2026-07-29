# SRP and DRY Review

## 1. Purpose

This review examines the current Iteration 1 implementation of Reading Compass against two design principles:

- **Single Responsibility Principle (SRP):** a class or module should have one clear reason to change.
- **Don't Repeat Yourself (DRY):** shared behaviour and knowledge should be represented once rather than duplicated.

The review covers the current Django model, forms, views, shared mixins and base template.

## 2. Review Summary

The current Iteration 1 implementation generally satisfies SRP and DRY. Responsibilities are divided among models, forms, views, templates and reusable mixins. No major violation was found that requires immediate refactoring before Iteration 2.

The strongest design decision is the use of `OwnedBookQuerysetMixin` to centralise owner-based filtering for list, detail, update and delete operations. This avoids repeated access-control code and reduces the risk of inconsistent privacy checks.

## 3. Class and Module Review

| Component | Main responsibility | SRP finding | DRY finding | Result |
| --- | --- | --- | --- | --- |
| `Book` model | Store book data, reading status choices and model-level behaviour | The class is focused on the book domain model. `__str__()` and `get_absolute_url()` are normal model behaviours. | Reading-status values are defined once using `TextChoices`. | Satisfies SRP and DRY |
| `RegistrationForm` | Validate account-registration input | Email normalisation and duplicate-email validation belong to registration-form validation. | It extends Django's `UserCreationForm` instead of reimplementing password validation. | Satisfies SRP and DRY |
| `BookForm` | Validate and configure editable book fields | The form is limited to user-editable book data and presentation-related form configuration. | Shared validation and widget configuration are defined once and reused by create and update views. | Satisfies SRP and DRY |
| `RegisterView` | Coordinate account creation and automatic login | The view handles one registration workflow. | It relies on `RegistrationForm` and Django authentication rather than duplicating their logic. | Satisfies SRP and DRY |
| `OwnedBookQuerysetMixin` | Restrict book queries to the authenticated owner | The mixin has one clear security responsibility. | Owner filtering is implemented once and reused by four views. | Strong SRP and DRY compliance |
| `BookListView` | Display the current user's books | The view only coordinates the list page. | It reuses the ownership mixin and Django `ListView`. | Satisfies SRP and DRY |
| `BookDetailView` | Display one owned book | The view only coordinates the detail page. | It reuses the ownership mixin and Django `DetailView`. | Satisfies SRP and DRY |
| `BookCreateView` | Create a book for the authenticated user | The view focuses on creation and server-side owner assignment. | It reuses `BookForm` and Django `CreateView`. | Satisfies SRP and DRY |
| `BookUpdateView` | Update one owned book | The view only coordinates update behaviour. | It reuses `BookForm`, the ownership mixin and Django `UpdateView`. | Satisfies SRP and DRY |
| `BookDeleteView` | Delete one owned book | The view only coordinates deletion and redirection. | It reuses the ownership mixin and Django `DeleteView`. | Satisfies SRP and DRY |
| `base.html` | Provide the shared page structure and navigation | The template contains site-wide layout rather than page-specific content. | Shared HTML structure, authentication navigation and message rendering are defined once. | Satisfies SRP and DRY |

## 4. SRP Findings

### 4.1 Model responsibility

The `Book` model stores the data and rules directly related to a book record. Reading-status options are nested inside the model because they form part of the book domain. URL generation and the readable string representation are small model-level behaviours and do not introduce an unrelated responsibility.

### 4.2 Form responsibility

`RegistrationForm` and `BookForm` separate input validation from request-handling logic. Duplicate-email checking is contained in `RegistrationForm.clean_email()`, while whitespace normalisation for book fields is contained in `BookForm`. This prevents validation rules from being spread across views and templates.

### 4.3 View responsibility

Each class-based view represents one HTTP workflow: register, list, detail, create, update or delete. The current views are small because Django generic views provide the common request-processing behaviour.

### 4.4 Access-control responsibility

`OwnedBookQuerysetMixin` has a single security responsibility: return only books owned by the authenticated user. Keeping this rule in a separate mixin makes the access policy visible and reusable.

## 5. DRY Findings

### 5.1 Reused ownership filtering

The following views require the same owner restriction:

- `BookListView`
- `BookDetailView`
- `BookUpdateView`
- `BookDeleteView`

Instead of repeating `Book.objects.filter(owner=self.request.user)` in every view, the project defines it once in `OwnedBookQuerysetMixin`.

### 5.2 Reused book form

Both book creation and book updating use `BookForm`. Editable fields, field widgets, status guidance and text cleaning therefore remain consistent across both workflows.

### 5.3 Reused Django framework behaviour

The project extends Django's existing generic views, authentication mixins and `UserCreationForm`. This avoids duplicating framework-level code for authentication, validation, form processing, object retrieval and redirection.

### 5.4 Reused site layout

`base.html` provides the shared document structure, stylesheet, navigation and message area. Individual templates only need to provide page-specific content through template blocks.

## 6. Minor Improvement Opportunities

No immediate refactoring is required, but the following improvements may become useful as the project grows:

1. The reading-status help text is currently stored inside `BookForm`. If the same explanation is later required in several templates, API responses or documentation pages, it should be moved to a shared constant or derived from the model choices.
2. `BookCreateView` assigns ownership directly in `form_valid()`. This is appropriate for the current scope. If several future create workflows need the same owner-assignment behaviour, an owner-assignment mixin could be introduced.
3. `RegistrationForm` imports Django's concrete `User` model. The current project uses Django's default user model, so this works. Using `get_user_model()` would make the form more adaptable if a custom user model is introduced later.
4. As templates grow, repeated form-field rendering could be moved into a reusable partial template. The current form is small, so this is not yet necessary.

These are maintainability suggestions rather than current SRP or DRY failures.

## 7. Conclusion

The Iteration 1 implementation has a clear separation of responsibilities:

- models represent stored domain data;
- forms validate user input;
- views coordinate individual request workflows;
- mixins centralise shared access-control behaviour;
- templates handle presentation;
- Django framework classes provide reusable infrastructure.

The code therefore satisfies SRP and DRY at the current project scale. The project should preserve these patterns during Iteration 2, especially when adding new book features, progress tracking or additional user workflows.
