#!/bin/sh
echo "Waiting for PostgreSQL to start..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting development server at http://127.0.0.1:8000/admin"

exec "$@"
