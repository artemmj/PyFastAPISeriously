from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.purchase.products.schemas import ProductBaseModelSchema


class OrderItemBase(BaseModel):
    product_id: int = None
    quantity: int


class OrderItem(BaseModel):
    id: int
    quantity: int
    product_id: int = None
    product: ProductBaseModelSchema = Field()
    model_config = ConfigDict(from_attributes=True)


class OrderBaseSchema(BaseModel):
    id: int = Field()
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem] = []
    model_config = ConfigDict(from_attributes=True)
