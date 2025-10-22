import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated, AsyncGenerator

from sqlalchemy import func, TIMESTAMP, Integer, inspect
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings

# engine = create_async_engine(url=settings.db_url)
# async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

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


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия с автоматическим коммитом."""
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия без автоматического коммита."""
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self, exclude_none: bool = False):
        """Преобразует объект модели в словарь."""
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)
            # Преобразование специальных типов данных
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, uuid.UUID):
                value = str(value)
            # Добавляем значение в результат
            if not exclude_none or value is not None:
                result[column.key] = value
        return result

    def __repr__(self) -> str:
        """Строковое представление объекта для удобства отладки."""
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"
