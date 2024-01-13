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

python manage.py makemigrations users
python manage.py makemigrations
python manage.py migrate

echo "checking for superuser"
if python manage.py shell -c "from users.models import User; print(User.objects.filter(email='admin@admin.com', is_superuser=True).exists())" | grep "True"; then
    echo "superuser is OK"
else
    echo "No superuser"
    python manage.py createsuperuser --email=admin@admin.com --noinput
    echo "Superuser admin/admin was created"
fi


python manage.py runserver 0.0.0.0:8000
