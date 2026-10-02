"""
report.py
---------
Pydantic schemas for Report generation and listing.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class GenerateReportRequest(BaseModel):
    workspace_id: str
    title: Optional[str] = "Weekly Product Intelligence Summary"
    report_type: Optional[str] = "weekly_intelligence"


class ReportResponse(BaseModel):
    report_id: str
    workspace_id: str
    title: str
    report_type: str
    summary: str
    key_metrics: dict[str, Any]
    sections: list[dict[str, Any]]
    created_at: datetime

