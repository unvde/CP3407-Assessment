# Reading Compass

Reading Compass is a deployed Django community for discovering books, managing a private reading shelf, sharing reviews and lists, receiving recommendations, and discussing books in moderated forums.

- **Live application:** https://reading-compass.onrender.com/
- **Evidence portal:** `docs/index.md`
- **Story-to-code traceability:** `docs/traceability.md`

## Delivered product

Readers can register and sign in, search Open Library by title, author or ISBN, import a shared catalogue record, maintain private reading statuses and notes, browse by category or trait, publish ratings and reviews, create public or private lists, view public profiles, receive dismissible recommendations, and participate in threaded forums. Staff-only tools support category maintenance, metadata refresh, public-content moderation and deployment checks.

## Three-iteration scope

| Iteration | Goal | Stories | Estimated effort |
| --- | --- | --- | ---: |
| 1 | Establish a secure personal reading foundation | #1 Account access; #2 catalogue search/import; #3 private shelf/statuses | 7 development-days |
| 2 | Add social discovery and curation | #4 category/trait discovery; #5 ratings/reviews; #6 lists/profiles | 7 development-days |
| 3 | Complete community engagement and delivery | #7 forums/replies; #8 recommendations; #9 moderation/deployment | 7 development-days |

The authoritative backlog is in [`docs/week2/requirements-backlog.md`](docs/week2/requirements-backlog.md). Each completed Story has one canonical GitHub Issue (#1–#9); later evidence-only duplicates are superseded by those Story Issues.

## Evidence by course stage

- **Weeks 1–2:** [proposal](docs/week1/project-proposal.md), [interview findings](docs/week2/interview-findings.md), [requirements backlog](docs/week2/requirements-backlog.md)
- **Weeks 3–5 / Iteration 1:** [plan](docs/week3/iteration-plan.md), [task breakdown](docs/week4/task-breakdown.md), [review and velocity](docs/week5/iteration-review.md), [completed Stories](docs/week5/user-stories/README.md)
- **Weeks 6–8 / Iteration 2:** [adjusted plan](docs/week6/practical-report.md), [test plan](docs/week7/test-plan.md), [test cases](docs/week7/test-cases.md), [review and velocity](docs/week8/iteration-2-review.md), [completed Stories](docs/week7/user-stories/README.md)
- **Weeks 8–9 / Iteration 3:** [plan](docs/week8/iteration-3-plan.md), [TDD specifications](docs/week8/test-specifications.md), [final acceptance](docs/week9/iteration-3-final-acceptance.md)
- **Design:** [architecture](docs/design/architecture.md), [database](docs/design/database-design.md), [interface](docs/design/interface-design.md)

## Technology

- Python 3.12, Django and Django templates
- SQLite for local development; PostgreSQL on Render
- Gunicorn and WhiteNoise for production delivery
- Open Library Search, Subjects and Covers APIs
- Django test framework and GitHub Actions

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
python manage.py makemigrations --check
python manage.py test
```

## Deployment

`render.yaml` and `build.sh` define the Render deployment. Environment variables hold secrets and database configuration; migrations and static-file collection run during the build; `/health/` provides a lightweight health check. Demo content is seeded only when explicitly enabled.

## Team

- **Tianyang Zhang:** lead developer and technical lead
- **Yuhao Guo:** project coordination, requirements, documentation and QA
