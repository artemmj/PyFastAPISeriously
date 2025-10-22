import re
from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field, field_validator, model_validator

from src.auth.security import get_password_hash


class EmailModel(BaseModel):
    email: EmailStr = Field(description="Электронная почта")

    model_config = ConfigDict(from_attributes=True)


class RoleModelSchema(BaseModel):
    id: int = Field(description="Идентификатор роли")
    name: str = Field(description="Название роли")

    model_config = ConfigDict(from_attributes=True)


class UserModelBaseSchema(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    phone_number: str = Field(description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

    model_config = ConfigDict(from_attributes=True)

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value


class UserModelInfoSchema(UserModelBaseSchema):
    id: int = Field()
    role: RoleModelSchema = Field()

    # @computed_field
    # def role_name(self) -> str:
    #     return self.role.name

    # @computed_field
    # def role_id(self) -> int:
    #     return self.role.id


class UserModelRegisterSchema(UserModelBaseSchema):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    confirm_password: str = Field(min_length=5, max_length=50, description="Повторите пароль")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)  # хешируем пароль до сохранения в базе данных
        return self


class UserModelAuthSchema(EmailModel):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class UserModelUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=False)
