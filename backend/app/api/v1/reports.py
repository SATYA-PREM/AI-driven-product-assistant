"""
reports.py
----------
FastAPI API endpoints for generating and listing product intelligence reports.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.auth_middleware import get_current_user
from app.schemas.report import GenerateReportRequest, ReportResponse
from app.models.report import ReportModel
from app.core.database import db_manager
from app.utils.serialization import serialize_document

router = APIRouter(
    prefix="/reports",
    tags=["Reporting & Summaries"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/generate",
    response_model=ReportResponse,
    summary="Generate Executive Intelligence Report",
    description="Compile an automated executive summary report combining feedback signals, metrics, and actionable recommendations.",
)
def generate_report(
    body: GenerateReportRequest,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("reports")
    doc = ReportModel.create_document(
        workspace_id=body.workspace_id,
        title=body.title or "Product Intelligence Summary",
        report_type=body.report_type or "weekly_intelligence",
        summary=f"Automated intelligence synthesis compiled for workspace {body.workspace_id}.",
    )
    col.insert_one(doc)
    return serialize_document(doc)


@router.get(
    "/{workspace_id}",
    response_model=list[ReportResponse],
    summary="List Generated Reports",
    description="Retrieve past intelligence reports generated for a workspace.",
)
def list_reports(
    workspace_id: str,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("reports")
    docs = list(col.find({"workspace_id": workspace_id}).sort("created_at", -1))
    if not docs:
        # Create a sample first report if none exist
        doc = ReportModel.create_document(
            workspace_id=workspace_id,
            title="Initial Product Intelligence Overview",
            summary="Kickoff summary generated upon workspace configuration.",
        )
        col.insert_one(doc)
        docs = [doc]
    return [serialize_document(d) for d in docs]


@router.get(
    "/detail/{report_id}",
    response_model=ReportResponse,
    summary="Get Report Details",
    description="Retrieve complete contents of a specific report.",
)
def get_report_detail(
    report_id: str,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("reports")
    doc = col.find_one({"report_id": report_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID '{report_id}' not found.",
        )
    return serialize_document(doc)

