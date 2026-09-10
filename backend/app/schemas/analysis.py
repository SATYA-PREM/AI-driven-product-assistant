"""
analysis.py
-----------
Pydantic schemas for AI Analysis operations.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AnalysisTriggerRequest(BaseModel):
    dataset_id: str = Field(..., description="ID of the dataset with AI-preprocessed signals")
    workspace_id: str = Field(..., description="Workspace ID context")
    analysis_types: Optional[list[str]] = Field(
        default=["sentiment", "themes", "recommendations"],
        description="Types of analysis to run"
    )


class AnalysisResponse(BaseModel):
    analysis_id: str
    dataset_id: str
    workspace_id: str
    status: str
    summary: str
    sentiment_distribution: dict[str, float]
    top_themes: list[dict[str, Any]]
    recommendations: list[str]
    created_at: datetime

