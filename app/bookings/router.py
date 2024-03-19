from fastapi import APIRouter, Depends, status

from app.bookings.dao import BookingDAO
from app.bookings.services import BookingService
from app.bookings.shemas import SNewBooking, SBookingInfo
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("", description="Возвращает список всех бронирований пользователя")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", description="Добавляет новую бронь", status_code=status.HTTP_201_CREATED)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    return await BookingService.add_booking(
        user, booking.room_id, booking.date_from, booking.date_to
    )


@router.delete(
    "", description="Удаляет бронь пользователя", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
