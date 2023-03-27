from app.services.database.models.user import User
from app.services.database.schemas.user import UserCreate, User as UserOutput
from app.services.database.repositories.base import Base


class UserRepository(Base):
    model = User

    def __init__(self, session, password_hasher) -> None:
        super().__init__(session)
        self._password_hasher = password_hasher

    async def get_user(self, name: str) -> UserOutput:
        return await self._select_one(self.model.full_name == name)

    async def get_by_email(self, email: str) -> UserOutput:
        return await self._select_one(self.model.email == email)
