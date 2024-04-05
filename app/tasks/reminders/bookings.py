import smtplib

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.config import settings
from app.logger import logger
from app.tasks.email_templates import create_booking_reminder_template


async def remind_of_booking(days: int):
    bookings: list[Bookings] = await BookingDAO.find_need_to_remind(days)

    msg = []
    for booking in bookings:
        email_to = booking.user.email

        booking_data: dict = {"date_from": booking.date_from, "date_to": booking.date_to}

        message = create_booking_reminder_template(booking=booking_data, email_to=email_to, days=days)
        msg.append(message)

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        for message in msg:
            smtp_server.send_message(message)

    logger.info("Successfully sent reminding messages")
