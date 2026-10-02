"""
pydantic_validator.py
---------------------
Rigorous Pydantic v2-based validation and business rule enforcement
for customer feedback, reviews, and support ticket records ingested from CSV, JSON, and Excel.
"""

from __future__ import annotations

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo, ValidationError

from app.utils.date_utils import is_valid_date


class FeedbackRecordSchema(BaseModel):
    """Pydantic model for customer feedback records matching enterprise CSV format."""
    # Identification
    feedback_id: Optional[str] = Field(default=None, description="Unique feedback record identifier (e.g. FB001)")
    customer_id: Optional[str] = Field(default=None, description="Unique customer identifier")

    # Core feedback & Rating
    rating: int = Field(..., ge=1, le=5, description="Product rating from 1 to 5")
    feedback: Optional[str] = Field(default=None, description="Customer feedback comments")
    feedback_text: Optional[str] = Field(default=None, description="Customer feedback comments")

    # Dates & Timestamps
    feedback_date: Optional[str] = Field(default=None, description="Feedback submission date (e.g. YYYY-MM-DD)")
    date: Optional[str] = Field(default=None, description="Submission date")
    created_at: Optional[str] = Field(default=None, description="ISO timestamp of record creation")

    # Enterprise Classification Dimensions
    customer_segment: Optional[str] = Field(default=None, description="Customer segment (Enterprise, SMB, Mid-Market)")
    platform: Optional[str] = Field(default=None, description="Platform (Web App, Mobile App, API)")
    module: Optional[str] = Field(default=None, description="Product module (Checkout, Login, Dashboard, Search, etc.)")
    browser_or_client: Optional[str] = Field(default=None, description="Browser or client (Chrome 131, iOS 18, etc.)")
    device_or_os: Optional[str] = Field(default=None, description="Device or operating system (Windows 11, iPhone 15, etc.)")
    country: Optional[str] = Field(default=None, description="Customer country (USA, UK, India, etc.)")
    source: Optional[str] = Field(default=None, description="Feedback source (Email, Support Ticket, Survey, In-App)")
    customer_type: Optional[str] = Field(default=None, description="Customer type (Returning, Power User, New, Admin)")

    @field_validator("rating", mode="before")
    @classmethod
    def parse_rating(cls, v: Any) -> int:
        if v is None or str(v).strip() == "":
            raise ValueError("rating is required")
        try:
            val = float(v)
            if not val.is_integer():
                raise ValueError(f"rating must be a whole integer, got {v}")
            val_int = int(val)
            if not (1 <= val_int <= 5):
                raise ValueError(f"rating must be between 1 and 5, got {val_int}")
            return val_int
        except (TypeError, ValueError) as e:
            raise ValueError(f"rating must be an integer between 1 and 5: {e}")

    @model_validator(mode="before")
    @classmethod
    def normalize_and_validate(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. Identifier
            c_id = data.get("customer_id") or data.get("feedback_id")
            if not c_id or str(c_id).strip() == "":
                raise ValueError("customer_id or feedback_id is required")
            id_str = str(c_id).strip()
            data["customer_id"] = id_str
            data["feedback_id"] = id_str

            # 2. Feedback Text
            fb_text = data.get("feedback_text") or data.get("feedback")
            if not fb_text or str(fb_text).strip() == "":
                raise ValueError("feedback text cannot be empty")
            fb_str = str(fb_text).strip()
            if len(fb_str) < 3:
                raise ValueError("feedback text is too short to be meaningful (min 3 chars)")
            data["feedback"] = fb_str
            data["feedback_text"] = fb_str

            # 3. Date
            d_val = data.get("feedback_date") or data.get("date") or data.get("created_at")
            if d_val:
                d_str = str(d_val).strip()
                data["feedback_date"] = d_str
                data["date"] = d_str

        return data


class ReviewRecordSchema(BaseModel):
    """Pydantic model for product review records."""
    review_id: Optional[str] = Field(default=None)
    customer_id: Optional[str] = Field(default=None)
    rating: int = Field(..., ge=1, le=5, description="Review rating from 1 to 5")
    review_text: str = Field(..., min_length=3, description="Review comment")
    date: Optional[str] = Field(default=None)

    @field_validator("rating", mode="before")
    @classmethod
    def parse_rating(cls, v: Any) -> int:
        if v is None or str(v).strip() == "":
            raise ValueError("rating is required")
        try:
            val = int(float(v))
            return val
        except Exception:
            raise ValueError(f"rating must be a number between 1 and 5, got '{v}'")

    @field_validator("review_text", mode="before")
    @classmethod
    def check_review_text(cls, v: Any) -> str:
        if v is None or str(v).strip() == "":
            raise ValueError("review_text cannot be empty")
        s = str(v).strip()
        if len(s) < 3:
            raise ValueError("review_text is too short to be meaningful")
        return s


class SupportTicketRecordSchema(BaseModel):
    """Pydantic model for customer support ticket records."""
    ticket_id: Optional[str] = Field(default=None)
    customer_id: Optional[str] = Field(default=None)
    description: str = Field(..., min_length=3, description="Ticket description or customer issue")
    priority: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)

    @field_validator("description", mode="before")
    @classmethod
    def check_description(cls, v: Any) -> str:
        if v is None or str(v).strip() == "":
            raise ValueError("description cannot be empty")
        s = str(v).strip()
        if len(s) < 3:
            raise ValueError("description is too short")
        return s


class PydanticValidator:
    """Orchestrates Pydantic-based record validation across source types."""

    _SCHEMA_MAP = {
        "feedback": FeedbackRecordSchema,
        "review": ReviewRecordSchema,
        "support_ticket": SupportTicketRecordSchema,
    }

    def validate_record(self, data: dict, source_type: str = "feedback") -> tuple[bool, list[str], list[str]]:
        """
        Validate a raw record using the appropriate Pydantic schema and business rules.

        Returns:
            (is_valid, errors, warnings)
        """
        st_key = str(source_type).lower()
        if "review" in st_key:
            schema_cls = ReviewRecordSchema
        elif "ticket" in st_key or "support" in st_key:
            schema_cls = SupportTicketRecordSchema
        else:
            schema_cls = FeedbackRecordSchema

        errors = []
        warnings = []

        try:
            schema_cls.model_validate(data)
            return True, [], []
        except ValidationError as e:
            for err in e.errors():
                loc = ".".join(str(item) for item in err["loc"])
                msg = err["msg"]
                # Clean up pydantic messages for clean user-facing error logs
                clean_msg = f"Missing required field: {loc}" if "missing" in msg.lower() else f"Field '{loc}': {msg}"
                errors.append(clean_msg)

        return False, errors, warnings


pydantic_validator = PydanticValidator()

