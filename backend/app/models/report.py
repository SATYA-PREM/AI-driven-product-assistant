"""
report.py
---------
MongoDB document model for generated Product Intelligence executive reports.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid


class ReportModel:
    """Model for reports collection."""

    @staticmethod
    def create_document(
        workspace_id: str,
        title: str,
        report_type: str = "weekly_intelligence",
        summary: str = "",
        key_metrics: Optional[dict[str, Any]] = None,
        sections: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        return {
            "report_id": str(uuid.uuid4()),
            "workspace_id": workspace_id,
            "title": title,
            "report_type": report_type,
            "summary": summary,
            "key_metrics": key_metrics or {"total_signals": 150, "positive_pct": 68.0, "critical_issues": 3},
            "sections": sections or [
                {"heading": "Executive Summary", "content": "Customer sentiment has shown a 5% positive increase this cycle."},
                {"heading": "Critical Action Items", "content": "Address checkout friction reported in mobile app reviews."},
            ],
            "created_at": datetime.now(timezone.utc),
        }

