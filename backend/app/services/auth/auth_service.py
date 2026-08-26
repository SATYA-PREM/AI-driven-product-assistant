from fastapi import HTTPException, status
from bson import ObjectId

from app.core.database import users_collection
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.models.user import UserModel


class AuthService:

    @staticmethod
    def register(
        name: str,
        email: str,
        password: str
    ):

        email = email.lower().strip()

        existing_user = users_collection.find_one(
            {"email": email}
        )

        if existing_user:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        password_hash = hash_password(password)

        user_document = UserModel.create_document(
            name=name,
            email=email,
            password_hash=password_hash,
            role="user"
        )

        result = users_collection.insert_one(
            user_document
        )

        user_id = str(result.inserted_id)

        token = create_access_token(
            user_id=user_id,
            email=email,
            role="user"
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "role": "user",
                "is_active": True
            }
        }

    @staticmethod
    def login(
        email: str,
        password: str
    ):

        email = email.lower().strip()

        user = users_collection.find_one(
            {"email": email}
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(
            password,
            user["password_hash"]
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.get("is_active", False):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        user_id = str(user["_id"])

        token = create_access_token(
            user_id=user_id,
            email=user["email"],
            role=user.get("role", "user")
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "name": user["name"],
                "email": user["email"],
                "role": user.get("role", "user"),
                "is_active": user.get("is_active", True)
            }
        }

    @staticmethod
    def get_user_by_id(user_id: str):

        if not ObjectId.is_valid(user_id):

            return None

        user = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )

        if not user:

            return None

        return user