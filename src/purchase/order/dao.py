from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.auth.dao import UsersDAO
from src.dao.base_dao import BaseDAO
from src.purchase.exceptions import CartEmptyException
from src.purchase.order.models import Order, OrderItem


class OrdersDAO(BaseDAO):
    model = Order

    async def get_one(self, order_id: int) -> Order | None:
        """Получить заказ с товарами."""
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.items)
                .selectinload(OrderItem.product)
            )
            .where(self.model.id == order_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Order]:
        """Получить все заказы с товарами."""
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.items)
                .selectinload(OrderItem.product)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_user_order(self, user_id: int) -> List[Order]:
        """Получить заказы пользователя детально с товарами."""
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.items)
                .selectinload(OrderItem.product)
            )
            .where(self.model.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def add(self, user_id: int) -> Order:
        """Создать новый заказ для пользователя. Скопировать товары из корзины, ее очистить."""
        user = await UsersDAO(self._session).get_user_with_cart(user_id=user_id)
        if not user.cart.items:
            raise CartEmptyException

        new_order = self.model(user_id=user_id)
        self._session.add(new_order)
        await self._session.commit()

        order_items_dao = OrderItemsDAO(self._session)
        for item in user.cart.items:
            await order_items_dao.add(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        user.cart.items = []
        return await self.get_one(order_id=new_order.id)


class OrderItemsDAO(BaseDAO):
    model = OrderItem

    # async def get_by_cart_and_product(self, cart_id: int, product_id: int) -> OrderItem:
    #     query = select(self.model).filter_by(cart_id=cart_id, product_id=product_id)
    #     result = await self._session.execute(query)
    #     record = result.scalar_one_or_none()
    #     return record

    async def add(self, order_id: int, product_id: int, quantity: int = 1) -> OrderItem:
        new_instance = self.model(order_id=order_id, product_id=product_id, quantity=quantity)
        self._session.add(new_instance)
        await self._session.commit()
        return new_instance
