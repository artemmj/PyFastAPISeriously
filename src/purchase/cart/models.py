from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.base_model import Base


class Cart(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="cart")

    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id})"


class CartItem(Base):
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='uq_cart_product'),
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, cart_id: {self.cart_id}, product_id={self.product_id})"
