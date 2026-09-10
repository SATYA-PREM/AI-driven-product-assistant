"""
pm_validation.py
----------------
MongoDB document models for salvaged data candidate records and PM review validation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid


class SalvagedDataModel:
    """Model for salvaged records pending or approved by Product Managers."""

    @staticmethod
    def create_document(
        dataset_id: str,
        workspace_id: str,
        dirty_record_id: str,
        row_number: int,
        salvaged_text: str,
        source_type: str = "feedback",
        inferred_attributes: Optional[dict[str, Any]] = None,
        confidence_score: float = 0.8,
        status: str = "pending_pm_validation",  # 'pending_pm_validation', 'approved', 'rejected'
        pm_notes: str = "",
        reviewed_by: str = "",
    ) -> dict[str, Any]:
        """Create a salvaged data candidate document."""
        return {
            "salvage_id": str(uuid.uuid4()),
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "dirty_record_id": dirty_record_id,
            "row_number": row_number,
            "salvaged_text": salvaged_text,
            "source_type": source_type,
            "inferred_attributes": inferred_attributes or {},
            "confidence_score": confidence_score,
            "status": status,
            "pm_notes": pm_notes,
            "reviewed_by": reviewed_by,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

