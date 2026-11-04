#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Creates the first admin from environment variables (skipped if it already exists)
python manage.py createsuperuser --no-input || true
