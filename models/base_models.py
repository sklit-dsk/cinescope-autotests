import datetime
import re
from typing import Any, Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationInfo, field_validator, field_serializer
from constants.roles import Roles
from uuid import UUID

class TestUser(BaseModel):
    id: Optional[str] = None
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: Optional[list[str]] = [Roles.USER.value]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info: ValidationInfo) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    model_config = ConfigDict()
    
    @field_serializer("roles")
    def _serialize_roles(self, roles: list[str], _info: Any) -> list[str]:
        return [r.value if isinstance(r, Roles) else r for r in roles]

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: Optional[bool] = False
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value
    

class UserModel(BaseModel):
    id: UUID
    email: EmailStr
    fullName: str = Field(min_length=1)
    roles: List[Roles]

    model_config = ConfigDict(extra="forbid")

class AuthResponse(BaseModel):
    user: UserModel
    accessToken: str = Field(min_length=10)
    refreshToken: UUID
    expiresIn: int

    model_config = ConfigDict(extra="forbid")

    @field_validator("accessToken")
    def _check_jwt(cls, v: str) -> str:
        # простая проверка на JWT-структуру header.payload.signature
        if not re.match(r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$", v):
            raise ValueError("accessToken не похож на JWT")
        return v

    @field_validator("expiresIn")
    def _check_expires(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("expiresIn должен быть положительным")
        return v
    