from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional
from enum import Enum

class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class User(BaseModel):
    email: str  # Имя должно быть строкой
    fullName: str  # Возраст должен быть числом
    password: str  # Поле "совершеннолетие" должно быть булевым значением
    passwordRepeat: str = Field(..., min_length=8)
    banned: Optional[bool] = False
    verified: Optional[bool] = True
    roles: list[Roles]
    
    @field_validator("email")
    def check_email_and_password(cls, value):
        if '@' not in value:
            raise ValueError("email Должен содержать @")
        return value
        
