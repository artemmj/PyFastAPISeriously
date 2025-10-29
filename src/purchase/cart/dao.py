import loguru
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from src.dao.base_dao import BaseDAO
from src.purchase.cart.models import Cart, CartItem
from src.purchase.cart.schemas import CartItemBase, CartUserIdSchema
from src.purchase.exceptions import ItemInCartNotFoundException

logger = loguru.logger


class CartsDAO(BaseDAO):
    model = Cart

    async def get_all(self):
        """Получить все корзины с товарами."""
        stmt = (
            select(Cart)
            .order_by(self.model.id)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_user_cart(self, user_id: int):
        """Получить корзину пользователя детально с товарами."""
        stmt = (
            select(Cart)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
            .where(Cart.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, user_id: int) -> Cart:
        """Создать новую корзину для пользователя, если нет, или вернуть существующую."""
        exist_cart = await self.get_one_by_filters(CartUserIdSchema(user_id=user_id))
        if exist_cart:
            return exist_cart

        new_cart = self.model(user_id=user_id)
        self._session.add(new_cart)
        await self._session.commit()
        return new_cart

    async def add_product(self, cart_id: int, product_id: int) -> Cart:
        """Добавить товар в корзину (+1)."""
        cart = await self.get_one_by_id(id=cart_id)
        cart_items_dao = CartItemsDAO(self._session)

        cart_item = await cart_items_dao.get_by_cart_and_product(cart_id, product_id)
        if cart_item:
            await cart_items_dao.update(id=cart_item.id, values=CartItemBase(quantity=cart_item.quantity + 1))
            await self._session.commit()
        else:
            await cart_items_dao.add(cart_id, product_id)
        await self._session.refresh(cart)
        return cart

    async def remove_product(self, cart_id: int, product_id: int) -> Cart:
        """Убрать товар из корзины (-1)."""
        cart = await self.get_one_by_id(id=cart_id)
        cart_items_dao = CartItemsDAO(self._session)

        cart_item = await cart_items_dao.get_by_cart_and_product(cart_id, product_id)
        if cart_item:
            new_quantity = cart_item.quantity - 1
            if new_quantity == 0:
                await cart_items_dao.delete(cart_item.id)
            else:
                await cart_items_dao.update(id=cart_item.id, values=CartItemBase(quantity=new_quantity))
            await self._session.commit()
        else:
            raise ItemInCartNotFoundException

        await self._session.refresh(cart)
        return cart

    async def clear_products(self, user_id: int, cart_id: int) -> None:
        """Очистить корзину от всех товаров."""
        stmt = delete(CartItem).filter_by(cart_id=cart_id)
        await self._session.execute(stmt)
        await self._session.flush()
        return await self.get_user_cart(user_id)


class CartItemsDAO(BaseDAO):
    model = CartItem

    async def get_by_cart_and_product(self, cart_id: int, product_id: int) -> CartItem:
        query = select(self.model).filter_by(cart_id=cart_id, product_id=product_id).order_by(self.model.id)
        result = await self._session.execute(query)
        record = result.scalar_one_or_none()
        return record

    async def add(self, cart_id: int, product_id: int, quantity: int = 1) -> CartItem:
        new_instance = self.model(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self._session.add(new_instance)
        await self._session.commit()
        return new_instance
