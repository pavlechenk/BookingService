from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled"
    ],
)


celery_app.conf.beat_schedule = {
    "email.remind_booking_1day": {
        "task": "remind_booking_1day",
        "schedule": crontab(minute="0", hour="9"),
    },

    "email.remind_booking_3day": {
        "task": "remind_booking_3day",
        "schedule": crontab(minute="30", hour="15"),
    },
}
