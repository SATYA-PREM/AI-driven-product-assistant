"""
pm_validation.py
----------------
FastAPI API endpoints for Product Manager (PM) review of dirty/salvaged records,
candidate auditing, and promotion to production AI-preprocessed data.
"""

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.middleware.auth_middleware import get_current_user
from app.repositories.data_repository import data_repository
from app.services.preprocessing.preprocessing_service import preprocessing_service
from app.schemas.pm_validation import (
    SalvagedCandidateResponse,
    PMReviewRequest,
    PMReviewResponse,
    PMPromoteRequest,
    PMPromoteResponse,
)
from app.utils.serialization import serialize_document

router = APIRouter(
    prefix="/pm-validation",
    tags=["PM Validation & Salvage"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/candidates/{dataset_id}",
    response_model=list[SalvagedCandidateResponse],
    summary="List Salvaged Records Pending PM Review",
    description="Retrieve dirty data records that contain salvageable feedback and are awaiting PM approval.",
)
def list_salvaged_candidates(
    dataset_id: str,
    status_filter: Optional[str] = Query("pending_pm_validation", description="Filter by status: pending_pm_validation, approved, rejected"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user=Depends(get_current_user),
):
    records = data_repository.get_salvaged_records(
        dataset_id=dataset_id, status=status_filter, skip=skip, limit=limit
    )
    return [serialize_document(r) for r in records]


@router.post(
    "/audit/{dataset_id}",
    summary="Trigger Dirty Data Audit & Salvage Analysis",
    description="Analyze dirty records, filter out corrupted noise, package candidates with missing fields for PM review, and compute usability score.",
)
def audit_dirty_records(
    dataset_id: str,
    workspace_id: str = Query(..., description="Workspace ID context"),
    current_user=Depends(get_current_user),
):
    res = preprocessing_service.audit_and_salvage_dirty_data(
        dataset_id=dataset_id, workspace_id=workspace_id
    )
    return res


@router.post(
    "/review",
    response_model=PMReviewResponse,
    summary="Review Salvaged Candidate",
    description="Approve or reject a candidate salvaged record.",
)
def review_candidate(
    body: PMReviewRequest,
    current_user=Depends(get_current_user),
):
    action = body.action.lower().strip()
    if action not in ["approve", "reject"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be either 'approve' or 'reject'.",
        )

    new_status = "approved" if action == "approve" else "rejected"
    reviewer = current_user.get("email") or current_user.get("id") or "PM"

    success = data_repository.update_salvaged_status(
        salvage_id=body.salvage_id,
        status=new_status,
        pm_notes=body.pm_notes or "",
        reviewer=reviewer,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salvaged record with ID '{body.salvage_id}' not found.",
        )

    return PMReviewResponse(
        salvage_id=body.salvage_id,
        status=new_status,
        message=f"Candidate {new_status} successfully by {reviewer}.",
    )


@router.post(
    "/promote",
    response_model=PMPromoteResponse,
    summary="Promote Approved Salvaged Records to AI Preprocessed Store",
    description="Elevate approved candidate records into the main 'ai_preprocessed_data' collection so downstream agents can utilize them.",
)
def promote_salvaged_records(
    body: PMPromoteRequest,
    current_user=Depends(get_current_user),
):
    reviewer = current_user.get("email") or current_user.get("id") or "ProductManager"
    res = preprocessing_service.promote_salvaged_records(
        dataset_id=body.dataset_id,
        workspace_id=body.workspace_id,
        salvage_ids=body.salvage_ids,
        reviewer=reviewer,
    )
    return res

