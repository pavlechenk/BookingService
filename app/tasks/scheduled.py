import asyncio
from app.tasks.reminders.bookings import remind_of_booking

from app.tasks.celery_app import celery_app


@celery_app.task(name="remind_booking_1day")
def remind_booking_1day():
    asyncio.run(remind_of_booking(1))


@celery_app.task(name="remind_booking_3day")
def remind_booking_3day():
    asyncio.run(remind_of_booking(3))
