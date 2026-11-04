#!/usr/bin/env bash
set -e
git pull
pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py collectstatic --no-input
echo "Done. Now click Reload on the PythonAnywhere Web tab."
