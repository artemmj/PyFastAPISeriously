from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.dao.base_model import Base


class ProductCategory(Base):
    title: Mapped[str]

    products: Mapped[List['Product']] = relationship(
        'Product',
        back_populates='category',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id})'


class Product(Base):
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("productcategories.id"), nullable=False)
    title: Mapped[str]
    article: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]
    image_url: Mapped[str] = mapped_column(String, default=None, nullable=True)

    # Связь с CartItem (один ко многим)
    cart_items: Mapped[List['CartItem']] = relationship(
        'CartItem',
        back_populates='product',
        cascade='all, delete-orphan',
    )
    # Связь с OrderItem (один ко многим)
    orders: Mapped[List['OrderItem']] = relationship(
        'OrderItem',
        back_populates='product',
        cascade='all, delete-orphan',
    )
    category: Mapped["ProductCategory"] = relationship("ProductCategory", back_populates="products")

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'article': self.article,
            'price': self.price,
            'description': self.description,
        }
