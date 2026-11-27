"""Schemas Pydantic para Usuário."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Campos base do usuário."""
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr


class UserCreate(UserBase):
    """Schema para criação de usuário."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema para atualização de usuário (campos opcionais)."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema de resposta do usuário."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema de resposta do token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Dados decodificados do token."""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None