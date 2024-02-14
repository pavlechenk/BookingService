from datetime import date

from fastapi import APIRouter, Depends, status
from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.shemas import SBooking, SBookingInfo, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование'],

)


@router.get('', description='Возвращает список всех бронирований пользователя')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked


@router.delete('/{booking_id}', description='Удаляет бронь пользователя', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking: Bookings = await BookingDAO.find_by_id(booking_id)
    if booking.user_id == user.id:
        await BookingDAO.delete(booking_id)
