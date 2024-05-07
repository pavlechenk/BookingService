from typing import Union

from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email_or_username: Union[EmailStr, str]
    password: str
    
    
class UserChangePassword(BaseModel):
    current_password: str
    new_password: str
    repeat_new_password: str
    

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
    
class UserRegistration(UserBase):
    password: str
    
    
class UserUpdate(UserBase):
    pass
    
    
class UserUpdatePartial(UserBase):
    username: Union[str, None] = None
    email: Union[EmailStr, None] = None
    
    
class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Union[str, None] = None
    token_type: str = "cookie"
    

class UserShema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    
    
    model_config = ConfigDict(from_attributes=True)
