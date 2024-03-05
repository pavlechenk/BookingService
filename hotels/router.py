from datetime import date
from typing import Optional

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.services import HotelService
from app.hotels.shemas import SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", description="Возвращает список отелей по заданным параметрам")
@cache(expire=30)
async def get_hotels_by_location(
    location: str, date_from: date, date_to: date
) -> list[SHotelInfo]:
    return await HotelService.get_hotels_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}", description="Возвращает все данные по одному отелю")
async def get_hotel(hotel_id: int) -> Optional[SHotel]:
    return await HotelDAO.find_one_or_none(id=hotel_id)
