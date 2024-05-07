from datetime import datetime, timedelta

from email_validator import EmailNotValidError, validate_email
from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.users.dao import UserDAO
from app.users.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_timedelta: timedelta = timedelta(minutes=settings.JWT_TOKEN.access_token_expire_minutes)
) -> str:
    to_encode = token_data.copy()
    now = datetime.utcnow()
    expire = now + expire_timedelta
    to_encode.update({"type": token_type, "exp": expire, "iat": now})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        key=settings.JWT_TOKEN.private_key_path.read_text(),
        algorithm=settings.JWT_TOKEN.algorithm
    )
    
    return encoded_jwt
    

async def get_user(email_or_username: str):
    try:
        validate_email(email_or_username)
        return await UserDAO.find_one_or_none(email=email_or_username)
    except EmailNotValidError:
        return await UserDAO.find_one_or_none(username=email_or_username)


async def authenticate_user(email_or_username: str, password: str):
    user: Users = await get_user(email_or_username)
    
    if user and verify_password(password, user.hashed_password):
        return user
        
