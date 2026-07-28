# Reading Compass Sequence Diagram

## Add a Book to the Personal Reading List

The sequence illustrates the authenticated book-creation workflow, including server-side ownership assignment and validation.

```mermaid
sequenceDiagram
    autonumber
    actor Reader
    participant Browser
    participant Auth as Django Authentication
    participant View as BookCreateView
    participant Form as BookForm
    participant Model as Book
    participant DB as Database

    Reader->>Browser: Open Add Book page
    Browser->>Auth: Request authenticated route

    alt User is not authenticated
        Auth-->>Browser: Redirect to login page
    else User is authenticated
        Auth->>View: Forward request with current user
        View-->>Browser: Render empty BookForm
        Reader->>Browser: Enter title, author, status and pages
        Browser->>View: POST form with CSRF token
        View->>Form: Validate submitted fields

        alt Form is invalid
            Form-->>View: Validation errors
            View-->>Browser: Re-render form with errors
        else Form is valid
            Form-->>View: Valid unsaved Book
            View->>Model: Assign request.user as owner
            View->>Model: Save Book
            Model->>DB: INSERT book record
            DB-->>Model: Stored book ID
            Model-->>View: Saved Book
            View-->>Browser: Redirect to book details
            Browser-->>Reader: Display new private book
        end
    end
```

## Security Significance

- Authentication is checked before the create view is available.
- The browser cannot select the owner.
- `BookCreateView` assigns the authenticated user on the server.
- CSRF protection is included in the form submission.
- Validation occurs before data is stored.

## Related Ownership Flow

For viewing, editing and deleting an existing book, `OwnedBookQuerysetMixin` limits the queryset to:

```text
Book.objects.filter(owner=request.user)
```

If a user requests another user's book ID, Django returns `404 Not Found` rather than exposing the record.

