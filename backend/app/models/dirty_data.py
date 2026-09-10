"""
dirty_data.py
-------------
MongoDB document model for storing dirty, invalid, or corrupted records
detected during validation and normalization.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional


class DirtyDataModel:
    """Model for dirty_data collection."""

    @staticmethod
    def create_document(
        dataset_id: str,
        workspace_id: str,
        row_number: int,
        raw_record: dict[str, Any],
        validation_errors: list[str],
        defect_type: str = "validation_failed",
        missing_fields: Optional[list[str]] = None,
        extracted_text: str = "",
        is_salvageable: bool = False,
        salvage_reason: str = "",
        salvage_confidence: float = 0.0,
    ) -> dict[str, Any]:
        """
        Create a MongoDB document representing a dirty or rejected record.
        """
        return {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "row_number": row_number,
            "raw_record": raw_record,
            "validation_errors": validation_errors,
            "defect_type": defect_type,  # e.g., 'corrupted', 'missing_fields', 'duplicate', 'schema_mismatch'
            "missing_fields": missing_fields or [],
            "extracted_text": extracted_text,
            "is_salvageable": is_salvageable,
            "salvage_reason": salvage_reason,
            "salvage_confidence": salvage_confidence,
            "status": "rejected",
            "created_at": datetime.now(timezone.utc),
        }

