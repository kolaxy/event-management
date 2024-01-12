#!/bin/sh

set -e

ls -a
whoami
pwd

echo "Waiting for the psql to be ready"
while ! nc -z -w 1 postgres 5432; do
  echo "db is not ready"
  sleep 1
done

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000