from datetime import date, datetime, timedelta

from sqlalchemy import func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import SQLAlchemyDAO
from app.database import async_session_maker, async_session_maker_nullpool
from app.exceptions import RoomFullyBooked
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDAO(SQLAlchemyDAO):
    model = Bookings

    @classmethod
    async def find_need_to_remind(cls, days: int):
        tomorrow_date = (datetime.utcnow() + timedelta(days=days)).date()
        async with async_session_maker_nullpool() as session:
            query = (
                select(Bookings)
                .where(Bookings.date_from == tomorrow_date)
            )

            bookings = await session.execute(query)
            return bookings.scalars().all()

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Bookings.__table__.columns, Rooms.__table__.columns)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(Bookings.user_id == user_id)
            )

            bookings = await session.execute(query)
            return bookings.mappings().all()

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        try:
            async with async_session_maker() as session:
                get_rooms_left = cls.__get_rooms_left(room_id, date_from, date_to)

                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar()

                if rooms_left and rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(
                            Bookings.id,
                            Bookings.user_id,
                            Bookings.room_id,
                            Bookings.date_from,
                            Bookings.date_to,
                        )
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.mappings().one()
                else:
                    raise RoomFullyBooked
        except (SQLAlchemyError, Exception) as e:
            message = "Database Exc: " if isinstance(e, SQLAlchemyError) else "Unkwonk Exc: "
            message += "Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(message, extra=extra, exc_info=True)

    @staticmethod
    def __get_rooms_left(room_id, date_from, date_to):
        booked_rooms = (
            select(Bookings)
            .where(
                (Bookings.room_id == room_id)
                & ((Bookings.date_from <= date_to) & (Bookings.date_to >= date_from))
            )
            .cte("booked_rooms")
        )

        get_rooms_left = (
            select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                    "rooms_left"
                )
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.id == room_id)
            .group_by(Rooms.quantity, booked_rooms.c.room_id)
        )

        return get_rooms_left
