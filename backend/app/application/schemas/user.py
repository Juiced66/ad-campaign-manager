from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for reading user data (excluding password)."""
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Schema for updating an existing user (all fields optional)."""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
