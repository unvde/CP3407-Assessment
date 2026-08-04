# Development and Build Tools

Reading Compass uses a small set of tools with clear responsibilities. The
choices support a server-rendered application, deterministic testing and a
repeatable deployment without adding a separate frontend build system.

## Application framework

- **Python and Django** provide URL routing, authentication, forms, validation,
  ORM persistence, migrations, templates, security middleware and the test
  framework.
- **Django templates and CSS** render the responsive interface on the server.
  This avoids client-side state duplication for form-centred workflows.
- **SQLite** provides a zero-configuration local database. **PostgreSQL** is
  selected through `DATABASE_URL` for concurrent production persistence.

## External libraries and services

| Tool or library | Use in the project |
| --- | --- |
| `certifi` | Supplies the certificate authority bundle used for verified Open Library HTTPS requests |
| `dj-database-url` | Converts the production database URL into Django configuration |
| `psycopg2-binary` | PostgreSQL database driver used by the deployed application |
| Gunicorn | Runs the Django WSGI application in production |
| WhiteNoise | Serves compressed, manifest-versioned static assets from the application |
| Open Library | Provides catalogue search, subject discovery and cover images |

Open Library calls are isolated in `books/services.py`, use a project
User-Agent and finite timeouts, and translate network or response failures into
a controlled application error. Signed, expiring import payloads prevent the
browser from silently changing imported catalogue metadata.

## Build and delivery

- `requirements.txt` defines compatible dependency ranges.
- `build.sh` installs dependencies, collects static files and applies database
  migrations. Demo content is optional and requires explicit environment
  variables.
- `render.yaml` records the web service, PostgreSQL service, health route,
  start command and production environment settings.
- GitHub Actions runs tests and deployment checks for repository changes.
- MkDocs builds this evidence site, and GitHub Pages publishes it from a
  separate documentation workflow using `docs-requirements.txt`.

## Development checks

The normal local verification commands are:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
mkdocs build --strict
```

These commands detect invalid Django configuration, model/migration drift,
behaviour regressions and broken documentation navigation before delivery.
