from datetime import date, timedelta

from app.exceptions import (CannotBookHotelForLongPeriod,
                            DateFromCannotBeAfterDateTo)
from app.hotels.dao import HotelDAO


class HotelService:
    @classmethod
    async def get_hotels_by_location(
        cls, location: str, date_from: date, date_to: date
    ):
        if date_from >= date_to:
            raise DateFromCannotBeAfterDateTo

        if date_to - date_from > timedelta(days=30):
            raise CannotBookHotelForLongPeriod

        return await HotelDAO.search_for_hotels(
            location=location, date_from=date_from, date_to=date_to
        )
