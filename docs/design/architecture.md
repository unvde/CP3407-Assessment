# Reading Compass Architecture Design

## Purpose

Reading Compass is a server-rendered Django application that combines a private
reading shelf with a shared catalogue, discovery, recommendations, public
reviews, reading lists and book forums. Request handling, validation,
persistence and presentation remain separated through Django's conventional
Model-Template-View structure.

## System Context and Deployment

```mermaid
flowchart LR
    Reader["Reader or staff member"]
    Browser["Web browser"]
    Render["Render HTTPS edge"]
    App["Gunicorn + Django WSGI"]
    DB[("PostgreSQL production database")]
    OL["Open Library search, subjects and covers"]
    Static["WhiteNoise static assets"]

    Reader --> Browser
    Browser -->|"HTTPS requests"| Render
    Render -->|"Forwarded HTTPS"| App
    App -->|"Django ORM"| DB
    App -->|"HTTPS JSON requests"| OL
    Browser -->|"Cover image requests"| OL
    App -->|"Compressed manifest assets"| Static
    Static --> Browser
```

Local development uses SQLite and Django's development server. Production uses
the `DATABASE_URL` supplied by Render, persistent PostgreSQL connections with
health checks, Gunicorn, HTTPS-aware settings and WhiteNoise compressed static
files. The `/health/` route provides a lightweight platform health check.

## Application Containers and Components

```mermaid
flowchart TB
    Browser["Browser"]

    subgraph Django["Reading Compass Django application"]
        Middleware["Security, sessions, CSRF, authentication and messages"]
        URLs["Project and books URL routing"]
        Views["Workflow views and permission mixins"]
        Forms["Input normalisation and validation"]
        Services["Open Library client, ranking and signed import tokens"]
        Models["Catalogue, shelf, community and forum models"]
        Templates["Server-rendered HTML templates"]
        StaticFiles["CSS and static assets"]
    end

    Database[("PostgreSQL / SQLite")]
    OpenLibrary["Open Library API"]

    Browser --> Middleware
    Middleware --> URLs
    URLs --> Views
    Views --> Forms
    Views --> Services
    Views --> Models
    Forms --> Models
    Models --> Database
    Services --> OpenLibrary
    Views --> Templates
    Templates --> Browser
    Templates --> StaticFiles
    StaticFiles --> Browser
```

## Component Responsibilities

| Component | Responsibility | Main implementation |
|---|---|---|
| URL configuration | Maps stable public, authenticated and staff routes | `reading_compass/urls.py`, `books/urls.py` |
| Views and permission mixins | Coordinates shelf, discovery, community, forum and moderation workflows; applies owner/author/staff scope | `books/views.py` |
| Forms | Normalises input and presents field-level validation | `books/forms.py` |
| Services | Calls Open Library, normalises/ranks results, handles failures and signs import payloads | `books/services.py` |
| Models | Stores shared catalogue, private shelf and community data; enforces relational rules | `books/models.py` |
| Templates | Renders accessible server-side pages and CSRF-protected forms | `templates/` |
| Static delivery | Provides the responsive visual system in development and production | `static/`, WhiteNoise |
| Authentication | Registration, login, logout, sessions and password validation | Django authentication plus `RegisterView` and `SafeLoginView` |
| Tests | Exercises models, services, views, permissions and complete workflows | `books/tests.py`, `books/test_*.py` |

## Catalogue Search and Import Flow

```mermaid
sequenceDiagram
    actor Reader
    participant Search as BookSearchView
    participant Service as Open Library service
    participant OL as Open Library
    participant Import as BookImportView
    participant DB as Database

    Reader->>Search: Search by title, author or ISBN
    Search->>Service: search_open_library(query)
    Service->>OL: HTTPS request with timeout and User-Agent
    OL-->>Service: JSON catalogue results
    Service-->>Search: Normalised and relevance-ranked results
    Search-->>Reader: HTML results with signed import tokens
    Reader->>Import: Token and selected shelf status
    Import->>Import: Validate status and verify signed token age
    Import->>DB: Upsert catalogue metadata and categories
    Import->>DB: Create or update the reader's shelf entry
    Import-->>Reader: Redirect to the private book detail
```

The import token contains only allow-listed metadata and is signed with a
dedicated salt. It expires after one hour. Reading status is checked against the
model choices before any catalogue or shelf record is written.

## Community and Permission Boundaries

```mermaid
flowchart LR
    Public["Anonymous visitor"]
    Member["Authenticated reader"]
    Owner["Record owner or author"]
    Staff["Staff member"]

    Public -->|"read"| Catalogue["Catalogue, public profiles, public lists, reviews and forums"]
    Member -->|"manage own"| Private["Shelf, notes, lists and dismissals"]
    Member -->|"create"| Community["Reviews, forum posts and replies"]
    Owner -->|"update or delete own"| Community
    Staff -->|"moderate and maintain"| Community
    Staff -->|"edit categories and refresh metadata"| Catalogue
```

- Private shelf and note queries are restricted to the signed-in owner.
- Reading-list edit operations require ownership; non-public lists are visible
  only to their owner.
- Review, post and reply changes require authorship or staff permission.
- Forum deletion, catalogue refresh, category maintenance and the moderation
  dashboard require staff access.
- Django CSRF protection guards state-changing forms; password hashing,
  session middleware, template escaping and clickjacking protection use Django
  defaults.
- Production settings derive secrets and hosts from the environment, trust the
  Render HTTPS proxy and can enable secure cookies and HSTS.

## Failure Handling

Open Library calls have finite timeouts and translate HTTP, network, timeout and
invalid-JSON failures into `BookSearchError`. Views show a controlled message or
fall back to locally stored catalogue data. Database constraints provide the
final defence against duplicate shelf entries, reviews, list names and
recommendation dismissals.

## Delivery Pipeline

```mermaid
flowchart LR
    Commit["Repository change"] --> CI["GitHub Actions"]
    CI --> Tests["Django tests and system checks"]
    CI --> Docs["MkDocs build"]
    Tests --> Build["Render build"]
    Build --> Install["Install dependencies"]
    Install --> Collect["Collect static files"]
    Collect --> Migrate["Apply migrations"]
    Migrate --> Deploy["Start Gunicorn"]
    Deploy --> Health["/health/ check"]
```

Demo data is not part of the normal build. It is seeded only when both explicit
demo password environment variables are present.

## Quality Attributes

| Attribute | Design response |
|---|---|
| Privacy | Owner-scoped private queries and visibility checks for lists |
| Integrity | Model validation, signed imports and database constraints |
| Availability | Managed deployment, health check and controlled external-service failures |
| Maintainability | Conventional Django layers and a dedicated external-service module |
| Testability | Isolated test database and deterministic mocked network boundaries |
| Accessibility | Semantic server-rendered HTML, labelled forms and responsive CSS |
| Evolvability | Versioned migrations and separate catalogue, shelf and community entities |
