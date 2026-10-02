from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.core.constants import UserRole


class RegisterRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    role: Optional[UserRole] = Field(
        default=UserRole.PRODUCT_MANAGER,
        description="Role preference: product_manager, data_engineer, product_designer, engineering_lead, customer_success"
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool


class TokenResponse(BaseModel):

    access_token: str
    token_type: str
    user: UserResponse