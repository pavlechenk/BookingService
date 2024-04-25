from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotActive,
    UserIsNotPresentException,
)
from app.users.dao import UserDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException

    return token


async def get_current_user(access_token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            access_token,
            key=settings.JWT_TOKEN.public_key_path.read_text(),
            algorithms=settings.JWT_TOKEN.algorithm
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user: Users = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    if not user.is_active:
        raise UserIsNotActive

    return user
