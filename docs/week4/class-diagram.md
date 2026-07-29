# Reading Compass Class Diagram

## 1. Purpose

This diagram describes the principal classes currently used by the Iteration 1 implementation. Django framework classes are included only where they clarify inheritance or collaboration.

```mermaid
classDiagram
    direction LR

    class User {
        +int id
        +string username
        +string email
        +check_password()
    }

    class Book {
        +int id
        +string title
        +string author
        +ReadingStatus status
        +int total_pages
        +datetime created_at
        +datetime updated_at
        +__str__()
        +get_absolute_url()
    }

    class ReadingStatus {
        <<enumeration>>
        WANT_TO_READ
        CURRENTLY_READING
        PAUSED
        COMPLETED
    }

    class RegistrationForm {
        +EmailField email
        +clean_email()
    }

    class BookForm {
        +clean_title()
        +clean_author()
    }

    class RegisterView {
        +form_valid(form)
    }

    class OwnedBookQuerysetMixin {
        +get_queryset()
    }

    class BookListView
    class BookDetailView
    class BookCreateView {
        +form_valid(form)
    }
    class BookUpdateView
    class BookDeleteView

    User "1" --> "0..*" Book : owns
    Book --> ReadingStatus : uses
    RegistrationForm --> User : creates
    BookForm --> Book : validates
    RegisterView --> RegistrationForm : uses
    BookCreateView --> BookForm : uses
    BookUpdateView --> BookForm : uses

    OwnedBookQuerysetMixin <|-- BookListView
    OwnedBookQuerysetMixin <|-- BookDetailView
    OwnedBookQuerysetMixin <|-- BookUpdateView
    OwnedBookQuerysetMixin <|-- BookDeleteView

    BookListView --> Book : queries
    BookDetailView --> Book : retrieves
    BookCreateView --> Book : creates
    BookUpdateView --> Book : updates
    BookDeleteView --> Book : deletes
```

## 2. Exported Diagram

The exported UML image is stored at [`diagrams/class-diagram.png`](diagrams/class-diagram.png).

![Reading Compass class diagram](diagrams/class-diagram.png)

## 3. Design Notes

- `User` is provided by Django's authentication system.
- Each `Book` has exactly one owner, while a user may own many books.
- `ReadingStatus` restricts status values to four valid choices.
- `BookForm` exposes only editable book fields; ownership is assigned by the server.
- `OwnedBookQuerysetMixin` filters queries by the authenticated user and prevents cross-user access.
- The class-based views separate list, detail, creation, update and deletion responsibilities.

## 4. Responsibility Review

The design keeps the current Iteration 1 responsibilities separated:

- Models define stored data and domain choices.
- Forms validate user input.
- Views coordinate HTTP workflows.
- Templates present information.
- Authentication and ownership checks protect private data.