from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCategoryBaseModelSchema(BaseModel):
    id: int = Field()
    title: str = Field(description='Название категории')
    model_config = ConfigDict(from_attributes=True)


class ProductCategoryCreateUpdateModelSchema(BaseModel):
    title: str = Field(description='Название категории')
    model_config = ConfigDict(from_attributes=True)


class ProductBaseModelSchema(BaseModel):
    id: int = Field()
    # category_id: int
    category: ProductCategoryBaseModelSchema
    title: str = Field(description='Название товара')
    article: str = Field(description='Артикул товара')
    price: float = Field(description='Цена товара')
    description: str = Field(description='Описание товара')
    image_url: Optional[str] = Field(None, description="URL изображения товара")
    model_config = ConfigDict(from_attributes=True)


class ProductCreateUpdateModelSchema(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    article: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
