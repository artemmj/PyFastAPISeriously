import loguru

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, get_current_admin_user
from src.auth.models import User
from src.dao.database import get_session, get_session
from src.purchase.products.dao import ProductCategoryDAO
from src.purchase.exceptions import FileSaveFailedException, IncorrectFileContentTypeException, ProductNotFoundException
from src.purchase.products.schemas import ProductCategoryBaseModelSchema, ProductCategoryCreateUpdateModelSchema
from src.purchase.products.models import ProductCategory

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_categories(
    # user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[ProductCategoryBaseModelSchema]:
    return await ProductCategoryDAO(session).find_all()


@router.post('')
async def create_category(
    category_data: ProductCategoryCreateUpdateModelSchema,
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> ProductCategoryBaseModelSchema:
    new_product = await ProductCategoryDAO(session).add(**category_data.model_dump(exclude_unset=True))
    return new_product


@router.put('/{id}')
@router.patch('/{id}')
async def update_product_category(
    id: int,
    new_product_data: ProductCategoryCreateUpdateModelSchema,
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> ProductCategoryBaseModelSchema:
    dao = ProductCategoryDAO(session)
    upd_cat = await dao.get_one_by_id(id=id)
    if not upd_cat:
        raise ProductNotFoundException
    await dao.update(id=id, values=new_product_data)
    await session.refresh(upd_cat)
    return upd_cat


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_category(
    id: int,
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    dao = ProductCategoryDAO(session)
    upd_cat = await dao.get_one_by_id(id=id)
    if not upd_cat:
        raise ProductNotFoundException
    return await dao.delete(id=id)
