#!/usr/bin/env bash
# Render Build Script — runs every time you deploy
# exit immediately on any error
set -o errexit

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Build complete!"
