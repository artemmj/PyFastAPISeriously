import loguru

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, get_current_admin_user
from src.auth.models import User
from src.dao.database import get_session, get_session
from src.purchase.order.dao import OrdersDAO
from src.purchase.order.schemas import OrderBaseSchema

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_orders(
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> List[OrderBaseSchema]:
    return await OrdersDAO(session).get_all()


@router.get('/my')
async def get_user_orders(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[OrderBaseSchema]:
    return await OrdersDAO(session).get_user_order(user_id=user.id)


@router.post('')
async def create_order(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> OrderBaseSchema:
    return await OrdersDAO(session).add(user_id=user.id)
