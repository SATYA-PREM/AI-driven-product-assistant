"""
ai_analysis.py
--------------
MongoDB document model for AI analysis results.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid


class AIAnalysisModel:
    """Model for ai_analyses collection."""

    @staticmethod
    def create_document(
        dataset_id: str,
        workspace_id: str,
        status: str = "completed",
        summary: str = "",
        sentiment_distribution: Optional[dict[str, Any]] = None,
        top_themes: Optional[list[dict[str, Any]]] = None,
        recommendations: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        return {
            "analysis_id": str(uuid.uuid4()),
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "status": status,
            "summary": summary,
            "sentiment_distribution": sentiment_distribution or {"positive": 0.65, "neutral": 0.20, "negative": 0.15},
            "top_themes": top_themes or [
                {"theme": "User Interface & Checkout", "mentions": 12, "sentiment": "negative"},
                {"theme": "Performance & Speed", "mentions": 28, "sentiment": "positive"},
            ],
            "recommendations": recommendations or [
                "Streamline the multi-step checkout workflow to decrease drop-off.",
                "Highlight recent performance enhancements in product changelog.",
            ],
            "created_at": datetime.now(timezone.utc),
        }

