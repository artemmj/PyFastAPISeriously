from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBaseModelSchema(BaseModel):
    title: str = Field(description='Название товара')
    article: str = Field(description='Артикул товара')
    price: float = Field(description='Цена товара')
    description: str = Field(description='Описание товара')

    model_config = ConfigDict(from_attributes=True)


class ProductUpdateModelSchema(BaseModel):
    title: Optional[str] = None
    article: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
