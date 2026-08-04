#!/usr/bin/env bash
set -o errexit

python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

if [[ -n "${DEMO_READER_PASSWORD:-}" && -n "${DEMO_ADMIN_PASSWORD:-}" ]]; then
    python manage.py seed_demo_content \
        --reader-password "$DEMO_READER_PASSWORD" \
        --admin-password "$DEMO_ADMIN_PASSWORD"
fi
