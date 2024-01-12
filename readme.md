```
CONTAINER ID   IMAGE                             COMMAND                  CREATED         STATUS         PORTS                    NAMES
f60c67fc89f0   mher/flower:latest                "celery flower"          6 minutes ago   Up 6 minutes   0.0.0.0:5555->5555/tcp   event_flower_container
8643e0057454   event_django_image:latest         "run.sh"                 6 minutes ago   Up 6 minutes   0.0.0.0:8000->8000/tcp   event_django_container
85bd4b765097   event_celeryworker_image:latest   "/start-celeryworker"    6 minutes ago   Up 6 minutes   8000/tcp                 event_celery_container
bac2e46e1be8   postgres:15.4-alpine3.18          "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes   0.0.0.0:5432->5432/tcp   event-management-postgres-1
e95135576fd3   redis:7.2.1-alpine3.18            "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes   6379/tcp                 event_redis_container
```