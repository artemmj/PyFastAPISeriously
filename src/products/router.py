import loguru

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.database import get_session_without_commit, get_session_with_commit
from src.products.dao import ProductsDAO
from src.products.exceptions import ProductNotFoundException
from src.products.schemas import ProductBaseModelSchema, ProductCreateModelSchema, ProductUpdateModelSchema

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_products(session: AsyncSession = Depends(get_session_without_commit)) -> List[ProductBaseModelSchema]:
    return await ProductsDAO(session).find_all()


@router.post('')
async def create_product(
    product_data: ProductCreateModelSchema,
    session: AsyncSession = Depends(get_session_with_commit),
) -> ProductBaseModelSchema:
    new_product = await ProductsDAO(session).add(**product_data.model_dump(exclude_unset=True))
    return new_product


@router.put('/{id}')
@router.patch('/{id}')
async def update_product(
    id: int,
    new_product_data: ProductUpdateModelSchema,
    session: AsyncSession = Depends(get_session_with_commit),
) -> ProductBaseModelSchema:
    dao = ProductsDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise ProductNotFoundException
    return await dao.update(id=id, values=new_product_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: int,
    session: AsyncSession = Depends(get_session_with_commit),
) -> None:
    dao = ProductsDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise ProductNotFoundException
    return await dao.delete(id=id)
