import pytest

from app.users.dao import UserDAO
from app.users.models import Users


@pytest.mark.parametrize(
    "user_id,email,user_exists",
    [
        (1, "test@test.com", True),
        (2, "Alex@gmail.com", True),
        (3, "crud@gmail.com", False),
    ],
)
async def test_find_user_by_id(user_id, email, user_exists):
    user: Users = await UserDAO.find_one_or_none(id=user_id)

    if user_exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
