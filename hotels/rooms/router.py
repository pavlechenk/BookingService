from datetime import date

from fastapi import APIRouter, Query

from app.hotels.rooms.shemas import SRoomInfo
from app.hotels.rooms.dao import RoomDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get("/{hotel_id}/rooms", description='Возвращает список всех номеров определенного отеля')
async def get_rooms(
        hotel_id: int,
        date_from: date = Query(default='2023-01-01'),
        date_to: date = Query(default='2023-12-31')
) -> list[SRoomInfo]:
    return await RoomDAO.find_all(hotel_id, date_from, date_to)
