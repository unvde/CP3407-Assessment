# Story 09 — Moderation and Production Delivery

**Issue:** [#9](https://github.com/unvde/CP3407-Assessment/issues/9)

**Iteration:** 3 · **Estimate:** 2 development-days · **Status:** Done

## Delivered behaviour

- A staff-only moderation centre lists forums, posts, replies, reviews and categories.
- Staff can rename/delete categories, refresh catalogue metadata and remove public content.
- Normal readers cannot enter moderation routes or be redirected there after login.
- Render deploys Django through Gunicorn with PostgreSQL, WhiteNoise, HTTPS-aware settings, migrations, static collection and `/health/`.
- Demo content seeding is idempotent and explicitly configured.

## Evidence

- Implementation: `StaffRequiredMixin`, moderation/category/refresh views, `render.yaml`, `build.sh` and production settings.
- Tests: moderation, category and demo-command tests plus `CommunityDiscoverySystemTests`.
- Delivery check: `python manage.py check --deploy`, migration drift, migration application, static collection and complete regression.
