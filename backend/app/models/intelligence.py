"""
intelligence.py
---------------
MongoDB document model for product intelligence metrics and sentiment tracking.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid


class IntelligenceModel:
    """Model for intelligence signals and metrics."""

    @staticmethod
    def create_document(
        workspace_id: str,
        product_id: Optional[str] = None,
        health_score: float = 85.5,
        nps_estimate: float = 42.0,
        positive_sentiment_pct: float = 68.0,
        negative_sentiment_pct: float = 14.0,
        neutral_sentiment_pct: float = 18.0,
        top_complaints: Optional[list[str]] = None,
        trending_features: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        return {
            "intelligence_id": str(uuid.uuid4()),
            "workspace_id": workspace_id,
            "product_id": product_id or "default",
            "health_score": health_score,
            "nps_estimate": nps_estimate,
            "sentiment": {
                "positive": positive_sentiment_pct,
                "negative": negative_sentiment_pct,
                "neutral": neutral_sentiment_pct,
            },
            "top_complaints": top_complaints or ["Slow export response", "Missing dark mode"],
            "trending_features": trending_features or ["AI search integration", "Bulk upload"],
            "updated_at": datetime.now(timezone.utc),
        }

