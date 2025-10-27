from src.auth.dao import UsersDAO
from src.dao.base_dao import BaseDAO
from src.purchase.order.models import Order


class OrdersDAO(BaseDAO):
    model = Order

    async def add(self, user_id: int) -> Order:
        """Создать новый заказ для пользователя."""
        user = await UsersDAO(self._session).get_user_with_cart(user_id=user_id)
        print(user.cart)

        new_order = self.model(user_id=user_id)
        self._session.add(new_order)
        await self._session.commit()
        return new_order
