# Reading Compass Architecture Design

## Purpose

Reading Compass uses a server-rendered Django architecture. The design keeps
presentation, request handling, validation and persistence responsibilities
separate while relying on Django's authentication and security middleware.

## System Context

```mermaid
flowchart LR
    Reader[Reader using a web browser]
    App[Reading Compass Django application]
    DB[(SQLite development database)]
    Static[Static CSS assets]

    Reader -->|HTTPS requests| App
    App -->|HTML responses| Reader
    App -->|Django ORM| DB
    App -->|Serves references to| Static
```

The deployed system should place an HTTPS reverse proxy or managed hosting
platform in front of Django. SQLite is appropriate for local development and
assessment demonstrations; a managed relational database should replace it if
the service grows or requires concurrent production writes.

## Container and Layer View

```mermaid
flowchart TB
    Browser[Browser]

    subgraph Django[Reading Compass Django Project]
        URLs[URL configuration]
        Views[Class-based views]
        Forms[Model forms and validation]
        Models[Book and ReadingNote models]
        Templates[Django templates]
        Auth[Django authentication]
        Middleware[Security, session and CSRF middleware]
    end

    Database[(Relational database)]
    CSS[Static CSS]

    Browser --> Middleware
    Middleware --> URLs
    URLs --> Views
    Views --> Auth
    Views --> Forms
    Forms --> Models
    Views --> Models
    Models --> Database
    Views --> Templates
    Templates --> Browser
    Templates --> CSS
```

## Component Responsibilities

| Component | Responsibility | Main implementation |
|---|---|---|
| URL configuration | Maps stable routes to views | `reading_compass/urls.py`, `books/urls.py` |
| Views | Coordinates authenticated request workflows and owner scoping | `books/views.py` |
| Forms | Normalises input and reports user-facing validation errors | `books/forms.py` |
| Models | Stores reading data and enforces domain validation | `books/models.py` |
| Templates | Renders accessible server-side HTML | `templates/` |
| Authentication | Registration, login, logout and session handling | Django auth plus `RegisterView` |
| Tests | Verifies model, form, view, privacy and integrated workflows | `books/tests.py`, `books/test_*.py` |

## Main Request Flow

```mermaid
sequenceDiagram
    actor Reader
    participant URL as URL Router
    participant View as Owner-scoped View
    participant Form as Django Form
    participant Model as Domain Model
    participant DB as Database
    participant Template as Template

    Reader->>URL: GET or POST request
    URL->>View: Dispatch matched route
    View->>View: Require authentication and scope by owner
    alt POST with form data
        View->>Form: Bind and validate input
        Form->>Model: Run model validation
        Model->>DB: Save valid owned record
    end
    View->>Template: Provide owned context
    Template-->>Reader: Render HTML response
```

## Security Boundaries

- Every book list, detail, edit and delete query is restricted to the signed-in
  owner.
- Reading-note and completion-review mutations also use owner-scoped queries.
- Django CSRF middleware and tokens protect state-changing forms.
- Django password hashing and authentication manage credentials and sessions.
- Templates escape user content by default.
- Production deployment must supply a secret key, disable debug mode, use
  HTTPS and enable secure session and CSRF cookies.

## Architectural Rationale

The project uses Django's conventional Model-Template-View structure because
it is small, form-centred and does not need a separate JavaScript API client.
Server-rendered pages reduce deployment and state-management complexity. The
owner-scoped query pattern keeps privacy enforcement close to every object
lookup, and reusable forms centralise validation across create and update
workflows.

## Quality Attributes

| Attribute | Design response |
|---|---|
| Privacy | Owner-scoped querysets and authenticated routes |
| Maintainability | Separate models, forms, views, URLs and templates |
| Testability | Deterministic Django tests with an isolated test database |
| Usability | Consistent cards, forms, status labels and navigation |
| Data integrity | Model/form validation and relational foreign keys |
| Evolvability | Django migrations and modular `books` application |

