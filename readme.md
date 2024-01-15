# Event management system

A Django REST API that allows users to create organizations, events and send text messages via WebSocket. Auth system - JWT

## Tech stack

- Docker, docker-compose
- Python 3.11.5
- Django 5.0
- Django Rest Framework 3.14.0
- Django Channels 4.0.0
- PostgreSQL 15.4-alpine3.18
- Redis 7.2.1-alpine3.18
- Celery latest
- Flower latest
- Swagger (drf-yasg 1.21.7)
- Pip

## Run in Docker
Start web application and database in Docker

```commandline
docker compose up
```

```
(venv) ➜  event-management git:(master) ✗ docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED             STATUS          PORTS                    NAMES
b12234dc3642   mher/flower:latest                "celery flower"          About an hour ago   Up 36 minutes   0.0.0.0:5555->5555/tcp   event_flower_container
422e91213236   event_celeryworker_image:latest   "/start-celeryworker"    About an hour ago   Up 36 minutes   8000/tcp                 event_celery_container
f1a59d4f2fe4   event_django_image:latest         "run.sh"                 About an hour ago   Up 36 minutes   0.0.0.0:8000->8000/tcp   event_django_container
7a90f9b6a95d   postgres:15.4-alpine3.18          "docker-entrypoint.s…"   About an hour ago   Up 36 minutes   0.0.0.0:5432->5432/tcp   event-management-postgres-1
440aa03b056c   redis:7.2.1-alpine3.18            "docker-entrypoint.s…"   38 hours ago        Up 36 minutes   6379/tcp                 event_redis_container
```

## App url

`localhost:8000`

Su user for admin panel is already created.

- Login `admin@admin.com`
- Password - `admin`

`localhost:8000/admin/`

Check swagger documentation

`localhost:8000/swagger/`

## Track celery tasks with Flower 

You can track celery tasks by Flower

`http://localhost:5555/`