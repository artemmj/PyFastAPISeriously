import loguru

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.dao.database import get_session_with_commit, get_session_without_commit
from src.purchase.order.dao import OrdersDAO
from src.purchase.order.schemas import OrderBaseSchema

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_orders(session: AsyncSession = Depends(get_session_without_commit)) -> List[OrderBaseSchema]:
    return await OrdersDAO(session).find_all()


@router.post('')
async def create_order(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    return await OrdersDAO(session).add(user_id=user.id)
