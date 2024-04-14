from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException, CannotAddDataToDatabase
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.shemas import SUserAuth

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_user = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase

    return {"message": "Пользователь успешно создан"}


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router_user.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router_user.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_user)):
    return await UserDAO.find_all()
