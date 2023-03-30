from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config.settings import Settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseManager:
    def __init__(self) -> None:
        self.SQLALCHEMY_DATABASE_URI = None
        self.engine = None
        self.session_factory = None

    def initialize(self, settings: Settings) -> None:
        self.settings = settings
        self.engine = create_async_engine(
            self.settings.SQLALCHEMY_DATABASE_URI, echo=True, pool_pre_ping=True)
        self.session_factory = scoped_session(sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False))

    async def get_db_session(self) -> Callable[..., AsyncSession]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
