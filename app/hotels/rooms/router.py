from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.shemas import SRoomInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "/{hotel_id}/rooms",
    description="Возвращает список всех номеров определенного отеля",
)
async def get_rooms(
    hotel_id: int,
    date_from: date = Query(
        description=f"Например, {datetime.now().date()}"
    ),
    date_to: date = Query(
        description=f"Например, {(datetime.now() + timedelta(days=14)).date()}",
    ),
) -> list[SRoomInfo]:
    return await RoomDAO.find_all(hotel_id, date_from, date_to)
