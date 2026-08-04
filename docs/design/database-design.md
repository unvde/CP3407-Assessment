# Reading Compass Database Design

## Entity-Relationship Diagram

```mermaid
erDiagram
    AUTH_USER ||--o{ BOOK : owns
    AUTH_USER ||--o{ CATALOG_BOOK : adds
    AUTH_USER ||--o{ CATEGORY : creates
    AUTH_USER ||--o{ PUBLIC_REVIEW : writes
    AUTH_USER ||--o{ READING_LIST : owns
    AUTH_USER ||--o{ RECOMMENDATION_DISMISSAL : dismisses
    AUTH_USER ||--o{ FORUM : creates
    AUTH_USER ||--o{ FORUM_POST : writes
    AUTH_USER ||--o{ FORUM_REPLY : writes

    CATEGORY }o--o{ CATALOG_BOOK : classifies
    CATALOG_BOOK ||--o{ BOOK : appears_on_shelf_as
    CATALOG_BOOK ||--o{ PUBLIC_REVIEW : receives
    CATALOG_BOOK }o--o{ READING_LIST : appears_in
    CATALOG_BOOK ||--o| FORUM : has
    BOOK ||--o{ READING_NOTE : contains
    FORUM ||--o{ FORUM_POST : contains
    FORUM_POST ||--o{ FORUM_REPLY : contains

    AUTH_USER {
        bigint id PK
        varchar username UK
        varchar email
        varchar password_hash
        boolean is_staff
        boolean is_active
        datetime date_joined
    }

    CATEGORY {
        bigint id PK
        varchar name UK
        varchar slug UK
        varchar source
        bigint created_by_id FK NULL
        datetime created_at
    }

    CATALOG_BOOK {
        bigint id PK
        varchar title
        varchar author
        varchar isbn_10
        varchar isbn_13
        varchar open_library_key UK NULL
        varchar cover_url
        varchar publisher
        smallint published_year NULL
        text description
        bigint added_by_id FK NULL
        datetime created_at
        datetime updated_at
    }

    BOOK {
        bigint id PK
        bigint owner_id FK
        bigint catalog_book_id FK NULL
        varchar title
        varchar author
        varchar status
        datetime created_at
        datetime updated_at
    }

    READING_NOTE {
        bigint id PK
        bigint book_id FK
        text content
        datetime created_at
        datetime updated_at
    }

    PUBLIC_REVIEW {
        bigint id PK
        bigint catalog_book_id FK
        bigint author_id FK NULL
        smallint rating
        text content
        datetime created_at
        datetime updated_at
    }

    READING_LIST {
        bigint id PK
        bigint owner_id FK
        varchar name
        text description
        boolean is_public
        datetime created_at
        datetime updated_at
    }

    RECOMMENDATION_DISMISSAL {
        bigint id PK
        bigint user_id FK
        varchar identifier
        datetime created_at
    }

    FORUM {
        bigint id PK
        bigint book_id FK UK
        varchar title
        text description
        bigint created_by_id FK NULL
        datetime created_at
    }

    FORUM_POST {
        bigint id PK
        bigint forum_id FK
        bigint author_id FK NULL
        varchar title
        text content
        datetime created_at
        datetime updated_at
    }

    FORUM_REPLY {
        bigint id PK
        bigint post_id FK
        bigint author_id FK NULL
        text content
        datetime created_at
        datetime updated_at
    }
```

Django creates junction tables for `CatalogBook.categories`,
`ReadingList.books` and the authentication permission relationships. They are
shown as many-to-many relationships rather than separate domain entities.

## Relationship and Lifecycle Rules

- A catalogue book is the shared identity used by community features. A private
  `Book` is a reader's shelf entry and keeps a title/author snapshot for manual
  entries and resilience if the shared record is later removed.
- A reader can place a catalogue book on their shelf only once. Manual shelf
  entries may have no `catalog_book` relationship.
- A reader can write at most one public review for each catalogue book and can
  own only one reading list with a given name.
- A catalogue book has at most one forum. Each forum contains posts, and each
  post contains chronological replies.
- Deleting a shelf entry cascades to its private notes. Deleting a catalogue
  book cascades to its reviews and forum, while linked shelf entries retain
  their snapshots because `catalog_book` uses `SET_NULL`.
- Community authors and creators use `SET_NULL`, preserving public content when
  an account is removed. Private shelf, list and dismissal records cascade with
  their owner.

## Domain Rules

| Rule | Enforcement |
|---|---|
| Reading status is `want_to_read`, `currently_reading`, `paused` or `completed` | `Book.ReadingStatus`, forms and import view validation |
| One linked shelf entry per reader and catalogue book | Conditional database unique constraint |
| Review rating is between 1 and 5 | Field validators |
| Review, note, post and reply text cannot be blank after trimming | Model validation; notes also have a database check constraint |
| One review per reader and catalogue book | Database unique constraint |
| One list name per owner | Database unique constraint |
| One forum per catalogue book | One-to-one relationship |
| One dismissal per user and recommendation identifier | Database unique constraint |
| Category names and slugs are unique | Unique fields and deterministic slug generation |
| Open Library work keys are unique when present | Nullable unique field |

## Normalisation and Design Decisions

The current schema separates the shared catalogue, private reading state and
public community data. Book metadata is stored once in `CatalogBook`; category
and reading-list membership use junction tables; repeatable notes, reviews,
posts and replies are separate entities. The limited title/author duplication
on `Book` is intentional: it supports manual entries and preserves a shelf
snapshot when a shared catalogue record is removed.

## Privacy and Indexing

Private shelves, notes, reading lists and recommendation dismissals are queried
through their owner. Public views expose catalogue metadata, reviews, public
lists and forum content only. Django indexes foreign keys automatically;
explicit indexes also support ISBN lookups. The existing unique constraints
cover the main ownership and deduplication paths. Additional composite or text
search indexes should be introduced only after measuring production queries.

## Migration Traceability

| Migration | Schema or data change | Current feature evidence |
|---|---|---|
| `0001_initial` | Creates the original owner-scoped `Book` shelf model | Private shelf foundation |
| `0002_book_current_page` | Adds page progress to the original model | Historical progress iteration |
| `0003_book_target_date` | Adds the original reading target field | Historical planning iteration |
| `0004_readingnote` | Adds repeatable private reading notes | `ReadingNote` model and note views |
| `0005_book_completion_date_book_rating_book_reflection` | Adds the original completion review fields | Historical completion-review iteration |
| `0006_category_forum_forumpost_catalogbook_and_more` | Adds shared catalogue, categories, forums and posts; migrates existing shelf metadata to catalogue records; links shelf entries; adds one-book-per-owner constraint | Catalogue import, explore and forum workflows |
| `0007_forumreply` | Adds threaded forum replies | Forum reply workflows |
| `0008_publicreview_readinglist_and_simplify_book` | Adds public reviews and reading lists; removes superseded page, target and completion-review fields from `Book` | Community reviews, lists and simplified shelf state |
| `0009_recommendationdismissal` | Adds persistent per-user recommendation dismissals | Dashboard recommendation controls |

`python manage.py makemigrations --check` is part of the release checks and
must report no difference between these committed migrations and the models.
