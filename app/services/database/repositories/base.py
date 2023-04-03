from abc import ABC
from typing import Any, Optional, Sequence, Type, Union
from sqlalchemy import delete, insert, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import MapperOption

from app.services.database.models import BaseModel as DBModel


class BaseRepository(ABC):
    model: Type[DBModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _insert(self, **kwargs: Any) -> DBModel:
        async with self.session as session:
            stmt = insert(self.model).values(**kwargs).returning(self.model)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def _update(self, *args: Any, **kwargs: Any) -> DBModel:
        async with self.session as session:
            stmt = update(self.model).where(
                *args).values(**kwargs).returning(self.model)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def _select_one(self, *args: Any) -> DBModel:
        async with self.session as session:
            stmt = select(self.model).where(*args)
            result = await session.scalar(stmt)
        return result

    async def _select_all(self, *args: Any) -> DBModel:
        async with self.session as session:
            stmt = select(self.model).where(*args)
            result = await session.scalars(stmt)
        return result.all()

    async def _delete(self, *args: Any) -> DBModel:
        async with self.session as session:
            stmt = delete(self.model).where(*args).returning(self.model)
            result = await session.scalar(stmt)
            await session.commit()
            print(result)
        return result
