# Testing Reading Compass

The test code is kept beside the Django application it verifies. The links
below open each test file directly.

## Test source code

| Test file | Tests | Main responsibility |
| --- | ---: | --- |
| [`books/tests.py`](books/tests.py) | 33 | Registration, authentication, shelf models, forms, ownership, status changes, dashboard, search and filters |
| [`books/test_community.py`](books/test_community.py) | 27 | Open Library services, signed imports, forums, replies, category maintenance and moderation |
| [`books/test_discovery.py`](books/test_discovery.py) | 11 | Reading lists, public profiles, recommendations, trait browsing, fallback and demo data |
| [`books/test_notes.py`](books/test_notes.py) | 13 | Reading-note validation, lifecycle, ownership and anonymous access |
| [`books/test_reviews.py`](books/test_reviews.py) | 6 | Rating constraints, review uniqueness, public visibility and permissions |
| [`books/test_system.py`](books/test_system.py) | 3 | Integrated reader journeys, privacy boundaries and anonymous write protection |
| **Complete suite** | **93** | All delivered components and workflows |

## Test levels

| Level | What is verified | Examples |
| --- | --- | --- |
| Model and form | Field constraints, normalisation, relationships and validation | rating range, unique review, blank note, trimmed book fields |
| Service | External request construction, certificate context, parsing, ranking, deduplication and failure handling | Open Library search and subject results |
| View and permission | Authentication, ownership, staff roles, redirects, messages and database effects | private shelves, list ownership, forum authorship, moderation |
| Acceptance | User-visible behaviour for every delivered capability | catalogue import, status filtering, public reviews, lists and trait discovery |
| System | Workflows crossing several components | shelf status, review and list journey; cross-reader privacy; anonymous writes |

## Representative regression coverage

- Valid imports create a shared catalogue book, categories and one private
  shelf entry.
- Duplicate imports reuse existing catalogue and shelf records.
- Tampered signed tokens and unsupported reading statuses are rejected without
  writing catalogue or shelf data.
- Readers cannot view or mutate another reader's private shelf, notes or lists.
- Public reviews are visible to anonymous visitors while review writes require
  authentication and author or staff permission.
- Trait search uses deterministic mocked Open Library results and falls back to
  the local catalogue when the provider fails.
- Recommendation dismissals persist and prevent the same suggestion from
  returning.
- Forum, post and reply permissions distinguish anonymous visitors, authors,
  other readers and staff.
- The demo-content command is idempotent and integrated workflows preserve
  privacy boundaries.

## Test data and external dependencies

Every Django `TestCase` receives a fresh test database. Test fixtures create
explicit reader, other-reader, anonymous and staff roles so privacy assertions
do not depend on shared state. Boundary values cover empty text, invalid rating
values, duplicate relationships, unknown statuses and tampered tokens.

Open Library is the only live external data dependency. Automated tests patch
the symbol used by the production service or view and return realistic JSON or
normalised results. This keeps parsing and application behaviour real while
removing network timing from the suite. The detailed rationale is documented
in [Mock Object Research](docs/week8/mock-object-research.md).

## Running the tests

Install the application dependencies, then run:

```bash
python manage.py test
```

Focused suites can be run by module:

```bash
python manage.py test books.test_community
python manage.py test books.test_discovery
python manage.py test books.test_notes
python manage.py test books.test_reviews
python manage.py test books.test_system
```

The full release gate is:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py check --deploy
```

## Continuous integration

The [Django tests workflow](https://github.com/unvde/CP3407-Assessment/actions/workflows/tests.yml)
runs on every push. It installs project dependencies, checks for missing
migrations, executes the complete Django suite and validates production
deployment settings.

The current `main` suite completes all 93 tests with no Django system-check or
migration-drift errors. Earlier test plans, selected cases and TDD
specifications remain in the weekly course record.
