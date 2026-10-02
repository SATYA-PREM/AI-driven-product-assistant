"""
tasks.py
--------
FastAPI API endpoints for actionable Product Tasks and backlog items.
"""

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.auth_middleware import get_current_user
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from app.models.task import TaskModel
from app.core.database import db_manager
from app.utils.serialization import serialize_document

router = APIRouter(
    prefix="/tasks",
    tags=["Product Tasks & Action Items"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=TaskResponse,
    summary="Create Actionable Task",
    description="Create a product engineering or design task stemming from customer feedback findings.",
)
def create_task(
    body: CreateTaskRequest,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("tasks")
    doc = TaskModel.create_document(
        workspace_id=body.workspace_id,
        title=body.title,
        description=body.description or "",
        priority=body.priority or "medium",
        assigned_to=body.assigned_to or "",
    )
    col.insert_one(doc)
    return serialize_document(doc)


@router.get(
    "/{workspace_id}",
    response_model=list[TaskResponse],
    summary="List Workspace Tasks",
    description="Retrieve all action items and tasks for a workspace.",
)
def list_tasks(
    workspace_id: str,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("tasks")
    docs = list(col.find({"workspace_id": workspace_id}).sort("created_at", -1))
    if not docs:
        doc = TaskModel.create_document(
            workspace_id=workspace_id,
            title="Investigate checkout latency",
            description="Generated from customer review mentions on slow billing response.",
            priority="high",
        )
        col.insert_one(doc)
        docs = [doc]
    return [serialize_document(d) for d in docs]


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update Task Status",
    description="Update task progress (todo, in_progress, done) or priority.",
)
def update_task(
    task_id: str,
    body: UpdateTaskRequest,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("tasks")
    updates = {}
    if body.status:
        updates["status"] = body.status
    if body.priority:
        updates["priority"] = body.priority
    if body.assigned_to:
        updates["assigned_to"] = body.assigned_to
    updates["updated_at"] = datetime.now(timezone.utc)

    res = col.find_one_and_update(
        {"task_id": task_id},
        {"$set": updates},
        return_document=True,
    )
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found.",
        )
    return serialize_document(res)

