from fastapi import APIRouter

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.services.auth.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=TokenResponse
)
def register(
    request: RegisterRequest
):

    role_val = request.role.value if hasattr(request.role, "value") else (request.role or "product_manager")
    return AuthService.register(
        name=request.name,
        email=request.email,
        password=request.password,
        role=role_val
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest
):

    return AuthService.login(
        email=request.email,
        password=request.password
    )