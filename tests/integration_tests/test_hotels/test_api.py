import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code,detail",
    [
        (
            "Алтай",
            "2023-06-20",
            "2023-06-10",
            400,
            "Дата заезда не может быть позже даты выезда",
        ),
        (
            "Алтай",
            "2023-06-10",
            "2023-07-22",
            400,
            "Невозможно забронировать отель сроком более месяца",
        ),
        ("Алтай", "2023-04-01", "2023-04-19", 200, None),
    ],
)
async def test_get_hotels_by_location(
    location, date_from, date_to, status_code, detail, async_client: AsyncClient
):
    response = await async_client.get(
        "/hotels",
        params={
            "location": location,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if str(status_code).startswith("4"):
        assert response.json()["detail"] == detail
