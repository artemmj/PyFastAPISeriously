from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.database import Base

# T = TypeVar("T")
T = TypeVar("T", bound=Base)


# class BaseDAO(Generic[T]):
#     model: Type[T] = None

#     def __init__(self, session: AsyncSession):
#         self._session = session
#         if self.model is None:
#             raise ValueError("Модель должна быть указана в дочернем классе")


class BaseRepository(ABC):
    @abstractmethod
    def get_first_by_kwargs(self, **kwargs):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args):
        pass


class SQLAlchemyRepository(BaseRepository, Generic[T]):
    model: T = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_first_by_kwargs(self, **kwargs) -> T:
        stmt = select(self.model).filter_by(**kwargs)
        return (await self.session.execute(stmt)).scalars().first()

    async def list(self) -> Sequence[T]:
        stmt = select(self.model)
        return (await self.session.execute(stmt)).scalars().all()

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        return instance

    async def update(self, row_id: int, update_data: dict[str | Any]) -> Result[int]:
        return await self.session.execute(
            update(self.model).where(self.model.id == row_id).values(**update_data).returning(self.model.id)
        )

    async def delete(self, row_id: int) -> Result[int]:
        return await self.session.execute(delete(self.model).where(self.model.id == row_id).returning(self.model.id))
