import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_picture(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized = image.resize((1000, 500))
    image_resized.save(f"app/static/images/resized_1000_500_{image_path.name}")


@celery_app.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    message = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        smtp_server.send_message(message)
