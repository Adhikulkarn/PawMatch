#!/usr/bin/env bash
# ==============================================================================
# PawMatch Render Build Script
# Executes installation, static collection, and database migrations on deploy
# ==============================================================================

set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing production dependencies..."
pip install -r requirements/production.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Executing database migrations..."
python manage.py migrate --noinput

echo "==> Build process completed successfully!"
