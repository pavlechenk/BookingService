from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expire_minutes: int = settings.JWT_TOKEN.access_token_expire_minutes
) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(
        to_encode, 
        key=settings.JWT_TOKEN.private_key_path.read_text(),
        algorithm=settings.JWT_TOKEN.algorithm
    )
    return encoded_jwt


async def authenticate_user(email: str, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user
