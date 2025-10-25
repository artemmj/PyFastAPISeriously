from sqlalchemy.orm import Mapped

from src.dao.base_model import Base


class Product(Base):
    title: Mapped[str]
    article: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'article': self.article,
            'price': self.price,
            'description': self.description,
        }
