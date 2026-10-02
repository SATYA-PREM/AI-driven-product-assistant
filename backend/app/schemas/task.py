"""
task.py
-------
Pydantic schemas for Action Tasks and Product Recommendations.
"""

from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    workspace_id: str
    title: str = Field(..., min_length=2)
    description: Optional[str] = ""
    priority: Optional[str] = "medium"
    assigned_to: Optional[str] = ""


class UpdateTaskRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str
    workspace_id: str
    title: str
    description: str
    priority: str
    status: str
    assigned_to: str
    created_at: datetime
    updated_at: datetime

