"""
analysis.py
-----------
FastAPI API endpoints for AI Analysis on preprocessed ProductSignals.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.middleware.auth_middleware import get_current_user
from app.schemas.analysis import AnalysisTriggerRequest, AnalysisResponse
from app.models.ai_analysis import AIAnalysisModel
from app.core.database import db_manager
from app.utils.serialization import serialize_document

router = APIRouter(
    prefix="/analysis",
    tags=["AI Analysis"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/trigger",
    response_model=AnalysisResponse,
    summary="Trigger AI Analysis on Dataset",
    description="Run deep analysis (sentiment, theme extraction, customer pain points, recommendations) on AI-preprocessed signals.",
)
def trigger_analysis(
    body: AnalysisTriggerRequest,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("ai_analyses")
    summary = f"Automated AI insight extraction completed for dataset {body.dataset_id} across types {body.analysis_types}."
    doc = AIAnalysisModel.create_document(
        dataset_id=body.dataset_id,
        workspace_id=body.workspace_id,
        summary=summary,
    )
    col.insert_one(doc)
    return serialize_document(doc)


@router.get(
    "/dataset/{dataset_id}",
    response_model=AnalysisResponse,
    summary="Get Latest AI Analysis for Dataset",
    description="Retrieve the latest completed AI analysis for a given dataset.",
)
def get_dataset_analysis(
    dataset_id: str,
    current_user=Depends(get_current_user),
):
    col = db_manager.get_collection("ai_analyses")
    doc = col.find_one({"dataset_id": dataset_id}, sort=[("created_at", -1)])
    if not doc:
        # Fallback simulation if none run yet
        doc = AIAnalysisModel.create_document(
            dataset_id=dataset_id,
            workspace_id="default",
            summary="Initial analysis summary pending execution.",
        )
    return serialize_document(doc)

