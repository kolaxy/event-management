import os
import time

from celery import shared_task
from app.celery import app
from .models import Event

CELERY_WAIT_TIME = os.getenv("CELERY_WAIT_TIME")


@app.task
def test_func():
    print("start")
    print("stop")


@app.task()
def create_event_with_delay(event_data):
    orgs = event_data.pop("organizations", None)
    event = Event.objects.create(**event_data)
    event.organizations.set(orgs)
    event.save()
