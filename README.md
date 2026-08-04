# Reading Compass

Reading Compass is a deployed Django community for discovering books, managing
a private reading shelf, sharing reviews and lists, receiving recommendations,
and discussing books in moderated forums.

- **Live application:** https://reading-compass.onrender.com/
- **Project evidence:** https://unvde.github.io/CP3407-Assessment/
- **Testing evidence:** [`docs/testing.md`](docs/testing.md)
- **Feature traceability:** [`docs/traceability.md`](docs/traceability.md)

## Delivered product

Readers can register and sign in, search Open Library by title, author or ISBN,
import a shared catalogue record, maintain private reading statuses and notes,
browse by category or trait, publish ratings and reviews, create public or
private lists, view public profiles, receive dismissible recommendations, and
participate in threaded forums. Staff-only tools support category maintenance,
metadata refresh, public-content moderation and deployment checks.

## Current evidence

| Area | Canonical evidence |
| --- | --- |
| Requirements and delivery scope | [Requirements backlog](docs/week2/requirements-backlog.md) and [feature traceability](docs/traceability.md) |
| Architecture, database and interface design | [Design documentation](docs/design/architecture.md) |
| Automated and acceptance testing | [Testing evidence](docs/testing.md) |
| Libraries, development and build tools | [Development tools](docs/development-tools.md) |
| Deployed implementation | [Live Reading Compass application](https://reading-compass.onrender.com/) |

## Iterative delivery

| Iteration | Goal | Delivered features | Estimated effort |
| --- | --- | --- | ---: |
| Foundation | Establish a secure personal reading foundation | Account access, catalogue import, private shelf and statuses | 7 development-days |
| Community | Add social discovery and curation | Trait discovery, ratings, reviews, lists and profiles | 7 development-days |
| Delivery | Complete community engagement and production readiness | Forums, recommendations, moderation and deployment | 7 development-days |

The weekly directories under `docs/` retain chronological course evidence.
They are supporting records rather than the primary navigation for the current
system.

## Technology

- Python, Django and Django templates
- SQLite for local development and PostgreSQL on Render
- Gunicorn and WhiteNoise for production delivery
- Open Library Search, Subjects and Covers APIs
- Django test framework and GitHub Actions
- MkDocs and GitHub Pages for project evidence

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_content
python manage.py runserver
```

Run verification with:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Deployment

`render.yaml` and `build.sh` define the Render deployment. Environment
variables hold secrets and database configuration; migrations and static-file
collection run during the build; `/health/` provides a lightweight health
check. Demo content is seeded only when explicitly enabled.

## Team

- **Tianyang Zhang:** lead developer and technical lead
- **Yuhao Guo:** project coordination, requirements, documentation and QA
