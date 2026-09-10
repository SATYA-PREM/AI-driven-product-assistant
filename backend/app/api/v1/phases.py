"""
phases.py
---------
FastAPI API endpoints for tracking milestone pipeline phases.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user
from app.schemas.phase import PhaseTransitionRequest, PhaseResponse
from app.models.phase import PhaseModel
from app.core.database import db_manager
from app.utils.serialization import serialize_document

router = APIRouter(
    prefix="/phases",
    tags=["Phases & Lifecycle"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/{workspace_id}",
    response_model=list[PhaseResponse],
    summary="List Pipeline Phases",
    description="Get current status of each phase (Ingestion, Validation, Cleaning, Preprocessing, Analysis).",
)
def get_phases(
    workspace_id: str,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("phases")
    docs = list(col.find({"workspace_id": workspace_id}))
    if not docs:
        # Default starter phases
        defaults = ["Ingestion", "Validation", "Cleaning", "Preprocessing", "AI Analysis"]
        docs = [
            PhaseModel.create_document(workspace_id=workspace_id, phase_name=p, status="completed" if i == 0 else "pending")
            for i, p in enumerate(defaults)
        ]
        col.insert_many(docs)
    return [serialize_document(d) for d in docs]


@router.post(
    "/transition",
    response_model=PhaseResponse,
    summary="Transition Phase Status",
    description="Update the execution status of a specific phase.",
)
def transition_phase(
    body: PhaseTransitionRequest,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("phases")
    doc = PhaseModel.create_document(
        workspace_id=body.workspace_id,
        phase_name=body.phase_name,
        status=body.status,
        metadata=body.metadata,
    )
    col.update_one(
        {"workspace_id": body.workspace_id, "phase_name": body.phase_name},
        {"$set": doc},
        upsert=True,
    )
    return serialize_document(doc)

