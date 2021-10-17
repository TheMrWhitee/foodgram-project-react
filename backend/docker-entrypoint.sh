#!/bin/bash

# Collect static
echo "Collect static files"
python manage.py collectstatic
# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

exec "$@"