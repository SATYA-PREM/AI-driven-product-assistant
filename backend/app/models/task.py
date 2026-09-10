"""
task.py
-------
MongoDB document model for action items, product backlog tasks, and Jira sync.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid


class TaskModel:
    """Model for tasks collection."""

    @staticmethod
    def create_document(
        workspace_id: str,
        title: str,
        description: str = "",
        priority: str = "medium",  # low, medium, high, critical
        status: str = "todo",  # todo, in_progress, done
        assigned_to: str = "",
    ) -> dict[str, Any]:
        return {
            "task_id": str(uuid.uuid4()),
            "workspace_id": workspace_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
            "assigned_to": assigned_to,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

