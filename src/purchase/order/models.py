from enum import Enum
from sqlalchemy import Enum as SqlEnum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.base_model import Base


class OrderStatus(Enum):
    PENDING = "На рассмотрении"
    PROCESSING = "В обработке"
    SHIPPED = "Отправлен"
    DELIVERED = "Доставлен"
    CANCELLED = "Завершен"


class Order(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)

    user: Mapped["User"] = relationship("User", uselist=True, back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id})"


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship('Product', back_populates='orders')

    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='uq_order_product'),
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, order_id: {self.order_id}, product_id={self.product_id})"
