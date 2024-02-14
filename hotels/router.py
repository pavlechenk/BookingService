from datetime import date
import asyncio
from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.shemas import SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=['Отели'])


@router.get("", description='Возвращает список отелей по заданным параметрам')
@cache(expire=20)
async def get_hotels_by_location(location: str, date_from: date, date_to: date) -> list[SHotelInfo]:
    await asyncio.sleep(3)
    return await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)


@router.get('/id/{hotel_id}', description='Возвращает все данные по одному отелю')
async def get_hotel(hotel_id: int) -> SHotel:
    return await HotelDAO.find_by_id(hotel_id)
