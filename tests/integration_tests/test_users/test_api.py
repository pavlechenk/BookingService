import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kot0pes", 409),
        ("pes@kpt.com", "pesokot", 200),
        ("abcde", "pesokot", 422),
    ],
)
async def test_register_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "string", 200),
        ("Alex@gmail.com", "string", 200),
        ("person@gmail.com", "string", 401),
    ],
)
async def test_login_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
