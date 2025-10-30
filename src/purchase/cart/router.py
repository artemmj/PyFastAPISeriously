import loguru

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.dependencies import get_current_user, get_current_admin_user
from src.dao.database import get_session, get_session
from src.purchase.cart.dao import CartsDAO
from src.purchase.cart.schemas import CartSchema, CartUserIdSchema
from src.purchase.exceptions import ProductNotFoundException
from src.purchase.products.dao import ProductsDAO

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_carts(
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> List[CartSchema]:
    return await CartsDAO(session).get_all()


@router.get('/my')
async def get_my_cart(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> CartSchema:
    carts_dao = CartsDAO(session)
    if not await carts_dao.get_one_by_filters(CartUserIdSchema(user_id=user.id)):
        await carts_dao.add(user_id=user.id)
    return await CartsDAO(session).get_user_cart(user.id)


@router.post('/add_product/{product_id}')
async def add_product(
    product_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> CartSchema:
    if not await ProductsDAO(session).get_one_by_id(id=product_id):
        raise ProductNotFoundException

    carts_dao = CartsDAO(session)
    cart = await carts_dao.get_user_cart(user_id=user.id)
    await carts_dao.add_product(cart.id, product_id)
    return await CartsDAO(session).get_user_cart(user.id)


@router.post('/remove_product/{product_id}')
async def remove_product(
    product_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> CartSchema:
    if not await ProductsDAO(session).get_one_by_id(id=product_id):
        raise ProductNotFoundException

    carts_dao = CartsDAO(session)
    cart = await carts_dao.get_one_by_filters(CartUserIdSchema(user_id=user.id))
    await carts_dao.remove_product(cart.id, product_id)
    return await carts_dao.get_user_cart(user.id)


@router.post('/clear_cart')
async def clear_cart(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    dao = CartsDAO(session)
    cart = await dao.get_one_by_filters(CartUserIdSchema(user_id=user.id))
    await dao.clear_products(user.id, cart.id)
    return cart
