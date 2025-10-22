from datetime import datetime, timezone
from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao import UsersDAO
from src.auth.models import User
from src.settings import settings
from src.dao.database import get_session_without_commit
from src.auth.exceptions import (
    TokenNoFound, NoJwtException, TokenExpiredException, NoUserIdException, ForbiddenException, UserNotFoundException
)


def get_access_token(request: Request) -> str:
    """Извлекаем access_token из хедеров."""
    token = request.headers.get('access_token')
    if not token:
        raise TokenNoFound
    return token


def get_refresh_token(request: Request) -> str:
    """Извлекаем refresh_token из хедеров."""
    token = request.headers.get('refresh_token')
    if not token:
        raise TokenNoFound
    return token


async def check_refresh_token(
    token: str = Depends(get_refresh_token),
    session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    """ Проверяем refresh_token и возвращаем пользователя."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise NoJwtException

    user_id = payload.get("sub")
    if not user_id:
        raise NoJwtException

    user = await UsersDAO(session).get_one_by_id(id=int(user_id))
    if not user:
        raise NoJwtException

    return user


async def get_current_user(
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    """Проверяем access_token и возвращаем пользователя."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO(session).get_one_by_id(id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Проверяем права пользователя как администратора."""
    if current_user.role.name == 'admin':
        return current_user
    raise ForbiddenException
