from typing import Union
from pydantic import BaseModel, EmailStr, ConfigDict


class SUserAuth(BaseModel):
    email_or_username: Union[EmailStr, str]
    password: str
    
    
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    

class UserShema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    
    
    model_config = ConfigDict(from_attributes=True)
