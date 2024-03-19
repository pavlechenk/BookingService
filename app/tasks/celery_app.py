from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["app.tasks.tasks"],
)
