import loguru

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.database import get_session_without_commit, get_session_with_commit
from src.products.dao import ProductsDAO
from src.products.schemas import ProductBaseModel

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_products(session: AsyncSession = Depends(get_session_without_commit)) -> List[ProductBaseModel]:
    return await ProductsDAO(session).find_all()


@router.post('')
async def create_product(
    product_data: ProductBaseModel,
    session: AsyncSession = Depends(get_session_with_commit),
) -> ProductBaseModel:
    new_product = await ProductsDAO(session).add(product_data)
    return new_product
