from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserResponse(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
