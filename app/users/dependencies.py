from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException

    return token


async def get_payload_token(access_token: str = Depends(get_token)):
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
    
    return payload


async def get_current_user(payload: dict = Depends(get_payload_token)):
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
