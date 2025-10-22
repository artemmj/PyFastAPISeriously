from pydantic import BaseModel, ConfigDict, Field


class ProductBaseModel(BaseModel):
    title: str = Field(description='Название товара')
    article: str = Field(description='Артикул товара')
    price: float = Field(description='Цена товара')
    description: str = Field(description='Описание товара')

    model_config = ConfigDict(from_attributes=True)
