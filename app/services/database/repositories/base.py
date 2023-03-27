from contextlib import asynccontextmanager
import typing
from abc import ABCMeta
from sqlalchemy import Executable, delete, exists, func, insert, lambda_stmt, select, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from sqlalchemy.orm import contains_eager, selectinload


ModelType = typing.TypeVar("ModelType")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]
ASTERISK = "*"


class Base(metaclass=ABCMeta):

    model = typing.ClassVar[typing.Type[ModelType]]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @asynccontextmanager
    async def __transaction(self) -> typing.AsyncGenerator:
        if not self._session.in_transaction() and self._session.is_active:
            async with self._session.begin() as transaction:
                yield transaction
        else:
            yield

    @property
    def _transaction(self) -> TransactionContext:
        return self.__transaction()

    def _convert_to_model(self, kwargs) -> ModelType:
        return self.model(**kwargs)

    async def _insert(self, **values: typing.Any) -> ModelType:
        async with self._transaction:
            stmt = insert(self.model).values(**values).returning(self.model)
            result = (await self._session.execute(stmt)).mappings().first()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result))

    async def _update(self, *conditions: typing.Any, **values: typing.Any) -> typing.Optional[ModelType]:
        async with self._transaction:
            stmt = update(self.model).where(
                *conditions).values(**values).returning(ASTERISK)
            result = (await self._session.execute(stmt)).mappings().first()
            await self._session.commit()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result)) if result is not None else None

    async def _select_all(self, *conditions: typing.Any) -> list[ModelType]:
        async with self._transaction:
            stmt = lambda_stmt(lambda: select(self.model))
            stmt += lambda s: s.where(*conditions)
            result = (await self._session.execute(typing.cast(Executable, stmt))).scalars().all()
        return result

    async def _select_one(self, *conditions: typing.Any) -> ModelType:
        async with self._transaction:
            stmt = lambda_stmt(lambda: select(self.model))
            stmt += lambda s: s.where(*conditions)
            result = (await self._session.execute(typing.cast(Executable, stmt))).scalars().first()
        return typing.cast(ModelType, result)

    async def _exists(self, *conditions: typing.Any) -> typing.Optional[bool]:
        async with self._transaction:
            subquery = select(self.model).where(*conditions)
            stmt = select(exists(subquery))
            result = await self._session.scalar(stmt)
        return bool(result)

    async def _delete(self, *conditions: typing.Any) -> None:
        async with self._transaction:
            stmt = delete(self.model).where(*conditions).returning(None)
            await self._session.execute(stmt)
            await self._session.commit()
        return None

    async def _filter(self, *conditions: typing.Any) -> typing.List[ModelType]:
        async with self._transaction:
            stmt = select(self.model).filter(*conditions)
            result = (await self._session.execute(stmt)).scalars().all()
        return result

    async def _count(self) -> int:
        async with self._transaction:
            count = (await self._session.execute(func.count(ASTERISK))).scalars().first()
        return typing.cast(int, count)

    async def _pagination(self, offset: int, limit: int) -> typing.List[ModelType]:
        async with self._transaction:
            stmt = select(self.model).offset(offset).limit(limit)
            result = (await self._session.execute(stmt)).scalars().all()
        return result

    async def _pagination_child(self, page: int, limit: int, key: int, order: typing.Any, filter_model: ModelType,
                                filter_order: typing.Any) -> ModelType:
        subq = select(filter_model). \
            filter(filter_order == key).offset(
            (page - 1) * limit).limit(
            limit).subquery().lateral()
        async with self._transaction:
            result = await self._session.execute(select(self.model).filter(order == key).outerjoin(subq).
                                                 options(contains_eager(self.model.products, alias=subq)))
        return result.scalars().first()

    async def _detail_one(self, order: typing.Any, value: typing.Any, clauses: typing.Tuple[typing.Any]) -> ModelType:
        stmt = list(map(lambda s: selectinload(s), clauses))
        async with self._transaction:
            result = await self._session.execute(
                select(self.model).order_by(order).filter(order == value).options(*stmt))
        return typing.cast(ModelType, result.scalars().first())

    async def _detail_list(self, offset: int, limit: int, order: typing.Any,
                           clauses: typing.Tuple[typing.Any]) -> typing.List[
            ModelType]:
        stmt = list(map(lambda s: selectinload(s), clauses))
        async with self._transaction:
            result = await self._session.execute(
                select(self.model).order_by(order).options(
                    *stmt).offset(offset).limit(limit))
        return result.scalars().all()
