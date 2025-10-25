import loguru

from fastapi import Query
from sqlalchemy import asc, desc, select
from sqlalchemy.exc import SQLAlchemyError

from src.auth.filters import UserFilter
from src.auth.exceptions import UserAlreadyExistsException
from src.auth.models import Role, User
from src.dao.base_dao import BaseDAO

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


class RolesDAO(BaseDAO):
    model = Role
