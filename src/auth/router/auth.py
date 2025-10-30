import loguru
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao import UsersDAO
from src.auth.exceptions import IncorrectEmailOrPasswordException
from src.auth.schemas import (
    AuthLoginSchema,
    EmailModel,
    UserModelAuthSchema,
    UserModelInfoSchema,
    UserModelRegisterSchema,
)
from src.auth.security import authenticate_user, set_tokens
from src.dao.database import get_session, get_session

router = APIRouter()
logger = loguru.logger


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserModelRegisterSchema,
    session: AsyncSession = Depends(get_session),
) -> UserModelInfoSchema:
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
    session: AsyncSession = Depends(get_session)
) -> AuthLoginSchema:
    dao = UsersDAO(session)
    user = await dao.get_one_by_filters(filters=EmailModel(email=user_data.email))

    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise IncorrectEmailOrPasswordException

    atoken, rtoken = set_tokens(response, user.id)
    return {
        'access_token': atoken,
        'refresh_token': rtoken,
    }
