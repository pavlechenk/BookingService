from fastapi import Request
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
from app.users.services import UserService


def get_user_service():
    return UserService(UserDAO)


def get_token(request: Request, token_name: str = "booking_access_token"):
    token = request.cookies.get(token_name)
    if not token:
        raise TokenAbsentException

    return token


def get_payload(token: str):
    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_TOKEN.public_key_path.read_text(),
            algorithms=settings.JWT_TOKEN.algorithm
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    
    return payload


async def get_current_user_by_token(payload: dict):
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user: Users = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    if not user.is_active:
        raise UserIsNotActive
    
    return user


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type
        self.__token_names: dict = {"access": "booking_access_token", "refresh": "booking_refresh_token"}
        
    async def __call__(self, request: Request):
        token = get_token(request, token_name=self.__token_names[self.token_type])
        payload = get_payload(token=token)
        current_token_type: str = payload.get("type")
        if current_token_type != self.token_type:
            raise IncorrectTokenFormatException(
                detail="Неверный тип токена"
            )
            
        return await get_current_user_by_token(payload=payload)
    

get_current_user = UserGetterFromToken(token_type="access")

get_current_user_for_refresh = UserGetterFromToken(token_type="refresh")

