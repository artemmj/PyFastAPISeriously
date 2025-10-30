from typing import List, TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.dao.base_model import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def get_one_by_id(self, id: int):
        """Получить одну запись по айди, либо None."""
        query = select(self.model).filter_by(id=id)
        result = await self._session.execute(query)
        record = result.scalar_one_or_none()
        return record

    async def get_one_by_filters(self, filters: BaseModel):
        """Получить одну запись по фильтрам, либо None."""
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        result = await self._session.execute(query)
        record = result.scalar_one_or_none()
        return record

    async def find_all(self, filters: BaseModel | None = None):
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        query = select(self.model).filter_by(**filter_dict).order_by(self.model.id)
        result = await self._session.execute(query)
        records = result.scalars().all()
        return records

    async def add(self, **kwargs):
        new_instance = self.model(**kwargs)
        self._session.add(new_instance)
        await self._session.commit()
        return new_instance

    async def add_many(self, instances: List[BaseModel]):
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        new_instances = [self.model(**values) for values in values_list]
        self._session.add_all(new_instances)
        await self._session.commit()
        return new_instances

    async def update(self, id: int, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        query = (
            sqlalchemy_update(self.model)
            .filter_by(id=id)
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(query)
        await self._session.commit()
        return await self.get_one_by_id(id=id)

    async def delete(self, id: int):
        query = sqlalchemy_delete(self.model).filter_by(id=id)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount

    async def count(self, filters: BaseModel | None = None):
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        query = select(func.count(self.model.id)).filter_by(**filter_dict)
        result = await self._session.execute(query)
        count = result.scalar()
        return count

    async def bulk_update(self, records: List[BaseModel]):
        updated_count = 0
        for record in records:
            record_dict = record.model_dump(exclude_unset=True)
            if 'id' not in record_dict:
                continue

            update_data = {k: v for k, v in record_dict.items() if k != 'id'}
            stmt = (
                sqlalchemy_update(self.model)
                .filter_by(id=record_dict['id'])
                .values(**update_data)
            )
            result = await self._session.execute(stmt)
            updated_count += result.rowcount

        await self._session.commit()
        return updated_count
