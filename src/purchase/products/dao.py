from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from src.dao.base_dao import BaseDAO
from src.purchase.products.models import Product, ProductCategory


class ProductsDAO(BaseDAO):
    model = Product

    async def get_one_by_id(self, id: int):
        query = select(self.model).options(
            selectinload(self.model.category)
        ).filter_by(id=id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def find_all(self, filters: BaseModel | None = None):
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}

        query = select(self.model).options(
            selectinload(self.model.category)
        ).filter_by(**filter_dict).order_by(self.model.id)

        result = await self._session.execute(query)
        records = result.scalars().all()
        return records

    async def add(self, **kwargs):
        new_instance = self.model(**kwargs)
        self._session.add(new_instance)
        await self._session.commit()
        stmt = select(self.model).options(selectinload(self.model.category)).where(self.model.id==new_instance.id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id: int, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        query = (
            update(self.model)
            .filter_by(id=id)
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(query)
        await self._session.flush()
        await self._session.commit()
        return await self.get_one_by_id(id=id)


class ProductCategoryDAO(BaseDAO):
    model = ProductCategory
