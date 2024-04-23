from pydantic import BaseModel, EmailStr, ConfigDict


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class UserShema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    
    
    model_config = ConfigDict(from_attributes=True)
