from datetime import date

from sqlalchemy import func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        query = (
            select(
                Hotels.__table__.columns,
                (Hotels.rooms_quantity - func.count(Bookings.room_id)).label(
                    "rooms_left"
                ),
            )
            .join(Rooms, Rooms.hotel_id == Hotels.id)
            .join(Bookings, Bookings.room_id == Rooms.id)
            .where(
                Hotels.location.like(f"%{location}%")
                & (Bookings.date_from <= date_to)
                & (Bookings.date_to >= date_from)
            )
            .group_by(Hotels.id, Hotels.rooms_quantity, Rooms.quantity)
            .having(func.count(Bookings.room_id) < Rooms.quantity)
        )

        async with async_session_maker() as session:
            hotels = await session.execute(query)
            return hotels.mappings().all()
