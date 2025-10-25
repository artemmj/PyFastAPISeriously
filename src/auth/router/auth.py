import loguru
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao import UsersDAO
from src.auth.exceptions import IncorrectEmailOrPasswordException
from src.auth.schemas import EmailModel, UserModelAuthSchema
from src.auth.security import authenticate_user, set_tokens
from src.dao.database import get_session_without_commit

router = APIRouter()
logger = loguru.logger


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
