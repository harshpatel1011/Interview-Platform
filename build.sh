#!/usr/bin/env bash
# Render Build Script — runs every time you deploy
# exit immediately on any error
set -o errexit

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Creating superuser (if not exists)..."
python manage.py createsuperuser --noinput || echo "Superuser already exists, skipping"

echo "==> Build complete!"
