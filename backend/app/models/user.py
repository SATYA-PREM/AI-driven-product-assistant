from datetime import datetime
from typing import Optional


class UserModel:

    @staticmethod
    def create_document(
        name: str,
        email: str,
        password_hash: str,
        role: str = "user"
    ):
        return {
            "name": name,
            "email": email.lower(),
            "password_hash": password_hash,
            "role": role,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }