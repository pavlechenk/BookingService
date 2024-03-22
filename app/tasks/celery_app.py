from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}",
    include=["app.tasks.tasks"],
)
