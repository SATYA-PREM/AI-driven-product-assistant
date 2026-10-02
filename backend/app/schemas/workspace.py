from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator


class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = ''


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str = ''
    owner_id: str = ''
    status: str = 'active'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(extra="ignore")


class MemberAdd(BaseModel):
    email: EmailStr
    role: str = 'member'


class MemberUpdate(BaseModel):
    role: str


class MemberResponse(BaseModel):
    id: Optional[str] = None
    user_id: str
    name: str = "Team Member"
    email: str = ""
    role: str = "member"
    joined_at: Optional[datetime] = None
    status: str = "active"
    user_name: Optional[str] = None
    user_email: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def populate_name_and_email(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize name
            name_val = data.get("name") or data.get("user_name") or "Team Member"
            data["name"] = name_val
            data["user_name"] = name_val

            # Normalize email
            email_val = data.get("email") or data.get("user_email") or ""
            data["email"] = email_val
            data["user_email"] = email_val

            # Normalize user_id
            if not data.get("user_id") and data.get("id"):
                data["user_id"] = str(data["id"])
        return data
