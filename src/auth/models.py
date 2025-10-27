from typing import List
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.base_model import Base, str_uniq
from src.purchase.cart.models import Cart


class Role(Base):
    name: Mapped[str_uniq]
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class User(Base):
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1, server_default=text("1"))
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")

    # Связь "один к одному" с CartSchema
    # uselist=False означает один к одному
    # cascade="all, delete-orphan" означает, что корзина удаляется вместе с пользователем
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")

    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates='user',
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self) -> dict:
        return {
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role_name': self.role.name,
        }
