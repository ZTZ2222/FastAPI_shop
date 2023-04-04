from typing import Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.models import User
from app.services.database.schemas.user import UserCreate, UserUpdate, GrantSuperUser
from ..base import BaseRepository
from app.utils.password_hashing import pwd_context


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self._password_hasher = pwd_context

    async def create_user(self, user: UserCreate) -> User:
        user.hashed_password = self._password_hasher.hash(user.password)
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

    async def get_all_users(self) -> Sequence[User]:
        return await self._select_all()

    async def activate_user(self, user: UserUpdate) -> User:
        payload = {"is_active": True}
        return await self._update(User.id == user.id, **payload)

    async def deactivate_user(self, user: UserUpdate) -> User:
        payload = {"is_active": False}
        return await self._update(User.id == user.id, **payload)

    async def delete_user(self, user: UserUpdate) -> User:
        return await self._delete(User.id == user.id)

    async def password_change_user(self, user: UserUpdate) -> User:
        payload = {
            "hashed_password": self._password_hasher.hash(user.password)}
        return await self._update(User.id == user.id, **payload)

    async def grant_admin_privileges(self, user: GrantSuperUser) -> User:
        return await self._update(User.email == user.email, **user.dict())
