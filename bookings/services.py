from datetime import date

from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.shemas import SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import Users


class BookingService:
    @classmethod
    async def add_booking(
        cls, user: Users, room_id: int, date_from: date, date_to: date
    ):
        booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
        if not booking:
            raise RoomCannotBeBooked

        booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
        send_booking_confirmation_email.delay(booking, user.email)

        return booking
