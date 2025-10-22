import loguru

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.auth.filters import UserFilter
from src.auth.schemas import (
    EmailModel,
    UserModelAuthSchema,
    UserModelInfoSchema,
    UserModelRegisterSchema,
    RoleModelSchema,
    UserModelUpdateSchema,
)
from src.auth.security import authenticate_user, set_tokens
from src.auth.dao import UsersDAO, RolesDAO
from src.dao.database import get_session_with_commit, get_session_without_commit
from src.exceptions import IncorrectEmailOrPasswordException, UserNotFoundException

router = APIRouter()
logger = loguru.logger


@router.get("/users/roles")
async def get_all_roles(session: AsyncSession = Depends(get_session_without_commit)) -> List[RoleModelSchema]:
    return await RolesDAO(session).find_all()


@router.get("/users", response_model=List[UserModelInfoSchema])
async def get_all_users(
    filters: UserFilter = Depends(),
    sorting: Optional[str] = Query(
        "id:asc", # Значение по умолчанию
        description="Поле и направление сортировки, например: 'name:asc', 'email:desc'"
    ),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await UsersDAO(session).find_all(filters=filters, sorting=sorting)


@router.get("/users/{id}", response_model=UserModelInfoSchema)
async def get_user_by_id(
    id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    instance = await UsersDAO(session).get_one_by_id(id=id)
    if not instance:
        raise UserNotFoundException
    return instance


@router.post("/users/register", response_model=UserModelInfoSchema, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserModelRegisterSchema,
    session: AsyncSession = Depends(get_session_with_commit),
):
    dao = UsersDAO(session)
    user_data_dict = user_data.model_dump()
    await dao.check_unique_user(user_data_dict.get('phone_number'), user_data_dict.get('email'))
    user_data_dict.pop('confirm_password', None)
    new_user = await dao.add(**user_data_dict)
    await session.refresh(new_user)
    return JSONResponse(new_user.to_dict(), status_code=status.HTTP_201_CREATED)


@router.post("/login")
async def login_user(
    response: Response,
    user_data: UserModelAuthSchema,
    session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    dao = UsersDAO(session)
    user = await dao.get_one_by_filters(filters=EmailModel(email=user_data.email))

    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise IncorrectEmailOrPasswordException

    atoken, rtoken = set_tokens(response, user.id)
    return {
        'access_token': atoken,
        'refresh_token': rtoken,
    }


@router.get("/me", response_model=UserModelInfoSchema)
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.put('/users/{id}')
@router.patch('/users/{id}')
async def update_user(
    id: int,
    new_user_data: UserModelUpdateSchema,
    session: AsyncSession = Depends(get_session_with_commit),
):
    dao = UsersDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise UserNotFoundException
    return await dao.update(id=id, values=new_user_data)


@router.delete('/users/{id}')
async def delete_user(
    id: int,
    session: AsyncSession = Depends(get_session_with_commit),
):
    dao = UsersDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise UserNotFoundException
    return await dao.delete(id=id)
