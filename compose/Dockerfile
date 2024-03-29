FROM python:3.11.5-alpine3.18

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts
COPY ./compose/celery/start /start-celeryworker

EXPOSE 8000

WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk update && \
    apk add --no-cache postgresql-client \
        build-base postgresql-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt --use-pep517 && \
    adduser --disabled-password --gecos '' djuser && \
    chown -R djuser:djuser /app && \
    mkdir -p /app/vol && \
    mkdir -p /app/vol /app/logs/info /app/logs/warning /app/logs/error /app/logs/critical && \
    chmod -R 755 /app && \
    chmod -R a+rw /app/logs/info /app/logs/warning /app/logs/error /app/logs/critical && \
    chmod -R +x /scripts && \
    chown -R djuser:djuser /start-celeryworker && \
    sed -i 's/\r$//g' /start-celeryworker && \
    chmod +x /start-celeryworker 

ENV PATH="/scripts:/py/bin:$PATH"

CMD ["run.sh"]
