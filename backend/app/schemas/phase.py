"""
phase.py
--------
Pydantic schemas for Pipeline Phase management.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PhaseTransitionRequest(BaseModel):
    workspace_id: str
    phase_name: str = Field(..., description="E.g. ingestion, validation, cleaning, preprocessing, ai_analysis")
    status: str = Field(..., description="E.g. in_progress, completed, failed")
    metadata: Optional[dict[str, Any]] = None


class PhaseResponse(BaseModel):
    phase_id: str
    workspace_id: str
    phase_name: str
    status: str
    metadata: dict[str, Any]
    updated_at: datetime

