from datetime import date

from sqlalchemy import select, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Bookings.__table__.columns,
                           Rooms.__table__.columns
            ).join(
                Rooms, Bookings.room_id == Rooms.id
            ).filter(Bookings.user_id == user_id)

            bookings = await session.execute(query)
            return bookings.mappings().all()

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            get_rooms_left = cls.__get_rooms_left(room_id, date_from, date_to)

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                new_booking = await super().add(room_id=room_id, user_id=user_id, date_from=date_from, date_to=date_to,
                                                price=price)
                return new_booking.scalar()

    @staticmethod
    def __get_rooms_left(room_id, date_from, date_to):
        booked_rooms = select(Bookings).where(
            (Bookings.room_id == room_id) &
            (
                    (Bookings.date_from <= date_to) &
                    (Bookings.date_to >= date_from)
            )
        ).cte("booked_rooms")

        get_rooms_left = select(
            (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
        ).select_from(Rooms).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).where(Rooms.id == room_id).group_by(
            Rooms.quantity, booked_rooms.c.room_id
        )

        return get_rooms_left
