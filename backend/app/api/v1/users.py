from fastapi import APIRouter, Depends

from app.middleware.auth_middleware import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_current_user_profile(
    current_user=Depends(get_current_user)
):

    return {
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "is_active": current_user["is_active"]
    }