"""
assistant_request.py
--------------------
MongoDB document model for Assistant interactions, natural language queries, and responses.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid


class AssistantRequestModel:
    """Model for assistant_requests collection."""

    @staticmethod
    def create_document(
        workspace_id: str,
        user_id: str,
        query: str,
        answer: str,
        cited_signals: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        return {
            "query_id": str(uuid.uuid4()),
            "workspace_id": workspace_id,
            "user_id": user_id,
            "query": query,
            "answer": answer,
            "cited_signals": cited_signals or [],
            "created_at": datetime.now(timezone.utc),
        }

