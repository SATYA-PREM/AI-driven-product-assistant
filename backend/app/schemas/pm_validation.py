"""
pm_validation.py
----------------
Pydantic schemas for Product Manager (PM) review of salvaged dirty records.
"""

from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class SalvagedCandidateResponse(BaseModel):
    """Candidate salvaged record awaiting or reviewed by PM."""
    salvage_id: str
    dataset_id: str
    workspace_id: str
    dirty_record_id: str
    row_number: int
    salvaged_text: str
    source_type: str = "feedback"
    inferred_attributes: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 0.8
    status: str = "pending_pm_validation"  # pending_pm_validation, approved, rejected
    pm_notes: str = ""
    reviewed_by: str = ""


class PMReviewRequest(BaseModel):
    """Request to approve or reject a salvaged candidate."""
    salvage_id: str
    action: str = Field(..., description="'approve' or 'reject'")
    pm_notes: Optional[str] = Field(default="", description="Optional PM rationale")


class PMReviewResponse(BaseModel):
    """Response after submitting PM review."""
    salvage_id: str
    status: str
    message: str


class PMPromoteRequest(BaseModel):
    """Request to promote approved salvaged records into the AI preprocessed stream."""
    dataset_id: str
    workspace_id: str
    salvage_ids: Optional[list[str]] = Field(
        default=None,
        description="Optional list of specific salvage IDs to promote. If omitted, all approved candidates are promoted."
    )


class PMPromoteResponse(BaseModel):
    """Summary of promoted signals."""
    dataset_id: str
    promoted_count: int
    status: str
    destination_collections: list[str]
    reviewed_by: str

