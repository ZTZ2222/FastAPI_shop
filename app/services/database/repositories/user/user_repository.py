from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.models import User
from app.services.database.schemas.user import UserCreate, UserUpdate
from ..base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        user.hashed_password = user.password
        del user.password
        return await self._insert(**user.dict(exclude_unset=True, exclude_none=True))

    async def update_user(self, user: UserUpdate) -> User:
        user.hashed_password = user.password
        del user.password
        return await self._update(User.id == user.id, **user.dict(exclude_unset=True, exclude_none=True))

    async def get_user_by_email(self, email: str) -> User:
        return await self._select_one(User.email == email)

    async def get_user_by_id(self, id: int) -> User:
        return await self._select_one(User.id == id)

    async def activate_user(self, user: UserUpdate) -> User:
        payload = {"is_active": True}
        return await self._update(User.id == user.id, **payload)

    async def deactivate_user(self, user: UserUpdate) -> User:
        payload = {"is_active": False}
        return await self._update(User.id == user.id, **payload)

    async def delete_user(self, user: UserUpdate) -> User:
        return await self._delete(User.id == user.id)

    # async def password_change_user(self, user: UserUpdate) -> User:
    #     payload = {"hashed_password": self._password_hasher.get_password_hash(user.password)}
    #     return await self._update(User.id == user.id, **payload)


class UserNotFoundError(Exception):
    entity_name: str = "User"

    def __init__(self, attr_name: str, attr_value: Any) -> None:
        message = f"{self.entity_name} with {attr_name} {attr_value} not found."
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    entity_name: str = "User"

    def __init__(self, attr_name: str, attr_value: Any) -> None:
        error_message = f"{self.entity_name} with {attr_name} {attr_value} already exists."
        super().__init__(error_message)
