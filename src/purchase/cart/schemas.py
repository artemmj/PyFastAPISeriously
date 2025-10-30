from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from src.purchase.products.schemas import ProductBaseModelSchema


class CartUserIdSchema(BaseModel):
    user_id: int


class CartItemBase(BaseModel):
    product_id: int = None
    quantity: int


class CartItem(BaseModel):
    id: int
    quantity: int
    product_id: int = None
    product: ProductBaseModelSchema

    model_config = ConfigDict(from_attributes=True)


class CartSchema(BaseModel):
    id: int
    user_id: int
    # created_at: datetime
    # updated_at: datetime
    items: List[CartItem] = []

    model_config = ConfigDict(from_attributes=True)
