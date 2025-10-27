import loguru

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao import RolesDAO, UsersDAO
from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.auth.filters import UserFilter
from src.auth.schemas import (
    RoleModelSchema,
    UserModelInfoSchema,
    UserModelRegisterSchema,
    UserModelUpdateSchema,
)
from src.dao.database import get_session_with_commit, get_session_without_commit
from src.auth.exceptions import UserNotFoundException

router = APIRouter()
logger = loguru.logger


@router.get('/about_me')
async def get_about_me(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit),
) -> UserModelInfoSchema:
    return await UsersDAO(session).get_user_with_cart(user.id)


@router.get("/roles")
async def get_all_roles(session: AsyncSession = Depends(get_session_without_commit)) -> List[RoleModelSchema]:
    return await RolesDAO(session).find_all()


@router.get('')
async def get_all_users(
    filters: UserFilter = Depends(),
    sorting: Optional[str] = Query(
        "id:asc", # Значение по умолчанию
        description="Поле и направление сортировки, например: 'name:asc', 'email:desc'"
    ),
    session: AsyncSession = Depends(get_session_without_commit),
) -> List[UserModelInfoSchema]:
    return await UsersDAO(session).find_all(filters=filters, sorting=sorting)


@router.get("/{id}")
async def get_user_by_id(
    id: int,
    session: AsyncSession = Depends(get_session_without_commit),
) -> UserModelInfoSchema:
    instance = await UsersDAO(session).get_user_with_cart(user_id=id)
    if not instance:
        raise UserNotFoundException
    return instance

@router.put('/{id}')
@router.patch('/{id}')
async def update_user(
    id: int,
    new_user_data: UserModelUpdateSchema,
    session: AsyncSession = Depends(get_session_with_commit),
) -> UserModelInfoSchema:
    dao = UsersDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise UserNotFoundException
    return await dao.update(id=id, values=new_user_data)


@router.delete('/{id}')
async def delete_user(
    id: int,
    session: AsyncSession = Depends(get_session_with_commit),
) -> None:
    dao = UsersDAO(session)
    del_user = await dao.get_one_by_id(id=id)
    if not del_user:
        raise UserNotFoundException
    return await dao.delete(user_id=id)
