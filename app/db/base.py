from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL, echo=settings.ENVIRONMENT == "development"
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class Database(ABC):
    @abstractmethod
    async def get_session(self) -> AsyncGenerator[Any, None]:
        pass

    @abstractmethod
    async def init_db(self) -> None:
        pass
