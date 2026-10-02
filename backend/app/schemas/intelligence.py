"""
intelligence.py
---------------
Pydantic schemas for Product Intelligence metrics, trends, and sentiment.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SentimentBreakdown(BaseModel):
    positive: float
    negative: float
    neutral: float


class IntelligenceSummaryResponse(BaseModel):
    intelligence_id: str
    workspace_id: str
    product_id: str
    health_score: float
    nps_estimate: float
    sentiment: SentimentBreakdown
    top_complaints: list[str]
    trending_features: list[str]
    updated_at: datetime

