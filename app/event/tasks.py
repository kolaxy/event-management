import time
from app.celery import app

@app.task
def test_func():
    time.sleep(10)