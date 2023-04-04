from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    full_name: Optional[str]
    password: Optional[str]
    hashed_password: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    telephone: Optional[str]


class UserCreate(UserUpdate):
    username: str
    email: EmailStr
    password: str


class UserResponse(UserBase):
    pass


class UserInDB(UserUpdate):
    pass


class GrantSuperUser(BaseModel):
    email: EmailStr
    is_superuser: bool
