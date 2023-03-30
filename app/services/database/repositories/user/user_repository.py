from typing import Any, Callable

from app.services.database.models.user import User
from app.services.database.schemas.user import UserCreate
from contextlib import AbstractAsyncContextManager
import typing
from abc import ABCMeta
from sqlalchemy import Executable, delete, exists, func, insert, lambda_stmt, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from app.services.database.schemas.user.user import UserInDBBase, UserUpdate

ASTERISK = "*"


class UserRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def user_create(self, user: UserCreate) -> User:
        async with self.session as session:
            payload = user.dict()
            payload["hashed_password"] = "fake_hashed_password"
            del payload["password"]
            stmt = insert(User).values(**payload).returning(User)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def user_update(self, user: UserUpdate) -> User:
        async with self.session as session:
            payload = user.dict()
            payload["hashed_password"] = "fake_hashed_password"
            del payload["password"]
            stmt = update(User).where(User.email == user.email).values(
                **payload).returning(User)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def get_user_by_email(self, email: str) -> User:
        async with self.session as session:
            stmt = lambda_stmt(lambda: select(User))
            stmt += lambda s: s.where(User.email == email)
            result = await session.scalar(stmt)
        return result

    async def get_user_by_id(self, id: int) -> User:
        async with self.session as session:
            stmt = lambda_stmt(lambda: select(User))
            stmt += lambda s: s.where(User.id == id)
            result = await session.scalar(stmt)
        return result

    async def user_activate(self, user: UserUpdate) -> User:
        async with self.session as session:
            payload = {"is_active": True}
            stmt = update(User).where(User.email == user.email).values(
                **payload).returning(User)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def user_deactivate(self, user: UserUpdate) -> User:
        async with self.session as session:
            payload = {"is_active": False}
            stmt = update(User).where(User.email == user.email).values(
                **payload).returning(User)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def user_delete(self, user: UserUpdate) -> User:
        async with self.session as session:
            stmt = delete(User).where(User.email == user.email).returning(User)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    # async def _filter(self, *conditions: typing.Any) -> typing.List[ModelType]:
    #     async with self.session_factory() as session:
    #         stmt = select(self.model).filter(*conditions)
    #         result = (await session.execute(stmt)).scalars().all()
    #     return result

    # async def _count(self) -> int:
    #     async with self.session_factory() as session:
    #         count = (await session.execute(func.count(ASTERISK))).scalars().first()
    #     return typing.cast(int, count)

    # async def _pagination(self, offset: int, limit: int) -> typing.List[ModelType]:
    #     async with self.session_factory() as session:
    #         stmt = select(self.model).offset(offset).limit(limit)
    #         result = (await session.execute(stmt)).scalars().all()
    #     return result

    # async def _pagination_child(self, page: int, limit: int, key: int, order: typing.Any, filter_model: ModelType,
    #                             filter_order: typing.Any) -> ModelType:
    #     subq = select(filter_model). \
    #         filter(filter_order == key).offset(
    #         (page - 1) * limit).limit(
    #         limit).subquery().lateral()
    #     async with self.session_factory() as session:
    #         result = await session.execute(select(self.model).filter(order == key).outerjoin(subq).
    #                                        options(contains_eager(self.model.products, alias=subq)))
    #     return result.scalars().first()

    # async def _detail_one(self, order: typing.Any, value: typing.Any, clauses: typing.Tuple[typing.Any]) -> ModelType:
    #     stmt = list(map(lambda s: selectinload(s), clauses))
    #     async with self.session_factory() as session:
    #         result = await session.execute(
    #             select(self.model).order_by(order).filter(order == value).options(*stmt))
    #     return typing.cast(ModelType, result.scalars().first())

    # async def _detail_list(self, offset: int, limit: int, order: typing.Any,
    #                        clauses: typing.Tuple[typing.Any]) -> typing.List[
    #         ModelType]:
    #     stmt = list(map(lambda s: selectinload(s), clauses))
    #     async with self.session_factory() as session:
    #         result = await session.execute(
    #             select(self.model).order_by(order).options(
    #                 *stmt).offset(offset).limit(limit))
    #     return result.scalars().all()

    # def _not_found_error_message(self, attribute_name: str, attribute_value: str) -> str:
    #     return f"{self.model.__name__} with {attribute_name} {attribute_value} not found."


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
