from datetime import date

from sqlalchemy import func, select

from app.bookings.models import Bookings
from app.dao.base import SQLAlchemyDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomDAO(SQLAlchemyDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        query = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),
                (Rooms.quantity - func.count(Bookings.room_id)).label("rooms_left"),
            )
            .select_from(Rooms)
            .join(Bookings, Bookings.room_id == Rooms.id, isouter=True)
            .where(Rooms.hotel_id == hotel_id)
            .group_by(Rooms.id)
        )

        async with async_session_maker() as session:
            rooms = await session.execute(query)
            return rooms.mappings().all()
