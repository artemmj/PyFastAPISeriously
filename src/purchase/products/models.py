from typing import List

from sqlalchemy.orm import Mapped, relationship

from src.dao.base_model import Base


class Product(Base):
    title: Mapped[str]
    article: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]

    # Связь с CartItem (один ко многим)
    cart_items: Mapped[List["CartItem"]] = relationship(
        "CartItem",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'article': self.article,
            'price': self.price,
            'description': self.description,
        }
