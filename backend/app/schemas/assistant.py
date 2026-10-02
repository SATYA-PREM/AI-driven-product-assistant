"""
assistant.py
------------
Pydantic schemas for AI Product Assistant chat and queries.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AskAssistantRequest(BaseModel):
    workspace_id: str = Field(..., description="Workspace ID context")
    query: str = Field(..., min_length=2, description="Natural language question about customer feedback, pain points, or roadmap")
    product_id: Optional[str] = Field(default=None, description="Optional product ID filter")


class AskAssistantResponse(BaseModel):
    query_id: str
    workspace_id: str
    query: str
    answer: str
    cited_signals: list[str]
    created_at: datetime

