"""
phase.py
--------
MongoDB document model for pipeline phase tracking.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import uuid


class PhaseModel:
    """Model for workflow phases."""

    @staticmethod
    def create_document(
        workspace_id: str,
        phase_name: str,
        status: str = "pending",  # pending, in_progress, completed, failed
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "phase_id": str(uuid.uuid4()),
            "workspace_id": workspace_id,
            "phase_name": phase_name,
            "status": status,
            "metadata": metadata or {},
            "updated_at": datetime.now(timezone.utc),
        }

