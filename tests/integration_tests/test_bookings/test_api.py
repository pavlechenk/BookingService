import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,booked_rooms,status_code",
    *[
        [(4, "2030-05-01", "2030-05-15", i, 201) for i in range(3, 11)]
        + [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
    ]
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    status_code,
    authenticated_async_client: AsyncClient,
):
    response = await authenticated_async_client.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response = await authenticated_async_client.get("bookings")

    assert len(response.json()) == booked_rooms


async def test_get_and_delete_bookings(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("bookings")

    existing_bookings = [booking["id"] for booking in response.json()]
    for booking_id in existing_bookings:
        response = await authenticated_async_client.delete(
            "/bookings", params={"booking_id": booking_id}
        )

        assert response.status_code == 204

    response = await authenticated_async_client.get("bookings")

    assert len(response.json()) == 0
