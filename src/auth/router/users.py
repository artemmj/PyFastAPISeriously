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


@router.get('/me')
async def get_me(user_data: User = Depends(get_current_user)) -> UserModelInfoSchema:
    return user_data


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
    instance = await UsersDAO(session).get_one_by_id(id=id)
    if not instance:
        raise UserNotFoundException
    return instance


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserModelRegisterSchema,
    session: AsyncSession = Depends(get_session_with_commit),
) -> UserModelInfoSchema:
    dao = UsersDAO(session)
    user_data_dict = user_data.model_dump()
    await dao.check_unique_user(user_data_dict.get('phone_number'), user_data_dict.get('email'))
    user_data_dict.pop('confirm_password', None)
    new_user = await dao.add(**user_data_dict)
    await session.refresh(new_user)
    return JSONResponse(new_user.to_dict(), status_code=status.HTTP_201_CREATED)


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
) -> int:
    dao = UsersDAO(session)
    del_user = await dao.get_one_by_id(id=id)
    if not del_user:
        raise UserNotFoundException
    return await dao.delete(id=id)
