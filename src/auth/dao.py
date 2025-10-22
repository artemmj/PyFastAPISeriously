import loguru

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import asc, desc, select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from src.auth.filters import UserFilter
from src.exceptions import UserAlreadyExistsException
from src.auth.models import Role, User
from src.dao.base import BaseDAO

logger = loguru.logger


class UsersDAO(BaseDAO):
    model = User

    async def find_all(self, filters: UserFilter, sorting: Query = None):
        """Находит всех юзеров, по фильтрам и с сортировкой."""
        query = select(self.model)

        # Фильтрация
        if filters.id:
            query = query.where(User.id == filters.id)
        if filters.first_name:
            query = query.where(User.first_name.ilike(f"%{filters.first_name}%"))
        if filters.last_name:
            query = query.where(User.last_name.ilike(f"%{filters.last_name}%"))
        if filters.email:
            query = query.where(User.email == filters.email)
        if filters.phone:
            query = query.where(User.phone == filters.phone)

        # Сортировка
        if sorting:
            sort_field_name, sort_direction = sorting.split(':') if ':' in sorting else (sorting, 'asc')
            sort_direction = sort_direction.lower()

            # Получаем атрибут модели SQLAlchemy по имени поля
            sort_column = getattr(User, sort_field_name, None)
            if sort_column is not None:
                # Применяем сортировку
                if sort_direction == 'desc':
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
            else:
                # Если поле сортировки не найдено, можно вернуть ошибку или использовать значение по умолчанию
                # Здесь просто игнорируем и используем сортировку по id (или какую-то другую)
                # raise HTTPException(status_code=422, detail=f"Поле сортировки '{sort_field_name}' не найдено.")
                pass # Продолжаем с сортировкой по умолчанию, если поле не найдено

        try:
            result = await self._session.execute(query)
        except SQLAlchemyError as e:
            raise e

        records = result.scalars().all()
        return records

    async def check_unique_user(self, phone: str, email: str):
        """Проверяет уникальность полей для регистрации юзера."""
        query_result = await self._session.execute(
            select(User).filter((User.email == email) | (User.phone_number == phone))
        )
        if query_result.scalar_one_or_none():
            raise UserAlreadyExistsException

    async def add(self, **kwargs):
        try:
            new_instance = self.model(**kwargs)
            self._session.add(new_instance)
            await self._session.flush()
            return new_instance
        except SQLAlchemyError as e:
            raise e

    async def update(self, id: int, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        query = (
            update(self.model)
            .filter_by(id=id)
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        result = await self._session.execute(query)

        try:
            await self._session.flush()
        except SQLAlchemyError as e:
            raise e

        return result.rowcount

    async def delete(self, id: int):
        query = delete(self.model).filter_by(id=id)
        result = await self._session.execute(query)

        try:
            await self._session.flush()
        except SQLAlchemyError as e:
            raise e

        return result.rowcount


class RolesDAO(BaseDAO):
    model = Role
