from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings

async_engine: AsyncEngine = create_async_engine(
    url=settings.db_url,
    # echo=DEV_MODE,
    pool_size=10,
    max_overflow=20,
)
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия с автоматическим коммитом."""
    async with session_factory() as session:
        try:
            yield session
        except Exception as exc:
            raise exc
        finally:
            await session.close()
