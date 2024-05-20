import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,username,password,status_code",
    [
        ("kot@pes.com", "kotpes", "kotopes", 201),
        ("kot@pes.com", "kotpes", "kot0pes", 409),
        ("pes@kpt.com", "peskot", "pesokot", 201),
        ("abcde", "abcde", "pesokot", 422),
    ],
)
async def test_register_user(email, username, password, status_code, async_client: AsyncClient):
    response = await async_client.post(
        "/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
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
        "/v1/auth/login",
        json={
            "email_or_username": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
