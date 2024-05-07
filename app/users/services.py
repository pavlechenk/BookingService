from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import Response, status
from pydantic import EmailStr

from app.config import settings
from app.dao.base import AbstractBaseDAO
from app.exceptions import (
    CannotAddDataToDatabase,
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
    UserIsNotPresentException,
    UserPasswordsDoNotMatch,
)
from app.users.auth import authenticate_user, create_jwt, get_password_hash, verify_password
from app.users.models import Users
from app.users.shemas import UserChangePassword, UserRegistration


class UserService:
    def __init__(self, user_dao: AbstractBaseDAO) -> None:
        self.user_dao = user_dao
        
        
    async def get_users(self, **filter_by):
        users = await self.user_dao.find_all(**filter_by)
        return users
    
    
    async def login_user(
        self,
        email_or_username: Union[EmailStr, str],
        password: str
    ):
        user = await authenticate_user(email_or_username, password)
        if not user:
            raise IncorrectEmailOrPasswordException

        data: dict = {"sub": str(user.id)}
        access_token = create_jwt(
            token_type="access",
            token_data=data,
        )
            
        refresh_token = create_jwt(
            token_type="refresh",
            token_data=data,
            expire_timedelta=timedelta(days=settings.JWT_TOKEN.refresh_token_expire_days)
        )
            
        return access_token, refresh_token
    
    
    async def set_cookie(self, response: Response, key: str, value: str):
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        
        expires: dict = {
            "booking_access_token": now + timedelta(minutes=settings.JWT_TOKEN.access_token_expire_minutes),
            "booking_refresh_token": now + timedelta(days=settings.JWT_TOKEN.refresh_token_expire_days)
        }
        
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,
            samesite='strict',
            expires=expires[key]
        )
 
    
    async def change_password(self, user_id: int, user_data: UserChangePassword):
        user: Union[Users, None] = await self.user_dao.find_one_or_none(id=user_id)
        
        if not user:
            raise UserIsNotPresentException
        
        if not verify_password(user_data.current_password, user.hashed_password):
            raise IncorrectEmailOrPasswordException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Введен неправильный пароль"
            )
            
        if user_data.new_password != user_data.repeat_new_password:
            raise UserPasswordsDoNotMatch
        
        
        hashed_password = get_password_hash(user_data.new_password)
        return await self.user_dao.update(user_id=user_id, hashed_password=hashed_password)
        
        
        
    async def create_user(self, user_data: UserRegistration):
        existing_user: Union[Users, None] = await self.user_dao.find_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        hashed_password = get_password_hash(user_data.password)
        new_user: Union[Users, None] = await self.user_dao.add(
            username=user_data.username, 
            email=user_data.email, 
            hashed_password=hashed_password
        )
        
        if not new_user:
            raise CannotAddDataToDatabase(detail="Не удалось добавить пользователя")

        return {
            "message": "Пользователь успешно создан"
        }
    
    
    async def update_user(self, user_id: int, **user_in: dict):
        user_id: Union[int, None] = await self.user_dao.update(user_id=user_id, **user_in)
        
        if not user_id:
            raise CannotAddDataToDatabase(detail="Не удалось обновить пользователя")
        
        return {
            "message": "Пользователь успешно обновлен"
        }
    
    
    async def delete_user(self, response: Response, user_id: int):
        user_id: Union[int, None] = await self.user_dao.delete(id=user_id)
        
        if not user_id:
            raise CannotAddDataToDatabase(detail="Не удалось удалить пользователя")
        
        response.delete_cookie("booking_access_token")
        response.delete_cookie("booking_refresh_token")

        return {
            "message": "Пользователь успешно удален"
        }
