#!/usr/bin/env bash
set -o errexit

# Install required Python packages
pip install -r requirements.txt

# Compile static files for WhiteNoise
python manage.py collectstatic --no-input

# Apply database migrations to Supabase
python manage.py migrate
