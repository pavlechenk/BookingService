from typing import Union
from fastapi import APIRouter, Depends, Response

from app.exceptions import CannotAddDataToDatabase, IncorrectEmailOrPasswordException, UserNotEnoughPrivileges
from app.users.auth import authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user, get_user_service
from app.users.models import Users
from app.users.services import UserService
from app.users.shemas import SUserAuth, UserChangePassword, UserRegistration, UserShema, UserUpdate, UserUpdatePartial
from fastapi import status

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_user = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegistration,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user_data=user_data)


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email_or_username, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token)
    return {"access_token": access_token}


@router_auth.post("/logout", dependencies=[Depends(get_current_user)])
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"message": "Вы успешно вышли из аккаунта"}


@router_auth.patch("/change_password")
async def change_password(
    user_data: UserChangePassword,
    current_user: Users = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    user_id: Union[int, None] = await user_service.change_password(current_user.id, user_data=user_data)
    
    if not user_id:
        raise CannotAddDataToDatabase(detail="Не удалось изменить пароль пользователя")
        
    return {
        "message": "Пароль был успешно изменен"
    }


@router_user.get("/me", response_model=UserShema)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router_user.get("/all", response_model=list[UserShema])
async def read_users_all(
    current_user: Users = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if not current_user.is_admin:
        raise UserNotEnoughPrivileges
    
    return await user_service.get_users()


@router_user.put("/me")
async def update_user_me(
    user_data: UserUpdate,
    current_user: Users = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.update_user(current_user.id, **user_data.model_dump())


@router_user.patch("/me")
async def update_user_partial_me(
    user_data: UserUpdatePartial,
    current_user: Users = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.update_user(current_user.id, **user_data.model_dump(exclude_none=True))


@router_user.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_service: UserService = Depends(get_user_service),
    current_user: Users = Depends(get_current_user)
):
    return await user_service.delete_user(user_id=current_user.id)
