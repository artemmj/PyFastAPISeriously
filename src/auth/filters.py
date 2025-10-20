from typing import Optional

from pydantic import BaseModel, Field


class UserFilter(BaseModel):
    id: Optional[int] = Field(None, description="Фильтр по id (точное совпадение)")
    first_name: Optional[str] = Field(None, description="Фильтр по имени (частичное совпадение)")
    last_name: Optional[str] = Field(None, description="Фильтр по имени (частичное совпадение)")
    email: Optional[str] = Field(None, description="Фильтр по email (точное совпадение)")
    phone: Optional[str] = Field(None, description="Фильтр по phone (точное совпадение)")

    class Config:
        extra = "forbid"  # запрещает передачу дополнительных полей
