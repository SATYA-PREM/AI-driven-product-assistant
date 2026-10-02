"""
tools.py
---------
Complete tool suite for the Preprocessing Agent covering:
1. Ingestion: customer feedback, reviews, support-tickets from CSV/JSON/Excel -> raw storage in MongoDB.
2. Pydantic Validation: schema validation, numeric bounds, text lengths, business rules.
3. Cleaning & Normalization: normalizing valid data into cleaned_data and isolating dirty data into dirty_data.
4. AI Preprocessing: rich understanding, intent detection, keywords -> ai_preprocessed_data.
5. Dirty Data Audit: separating corrupted noise from salvageable customer feedback.
6. PM Salvage Promotion: elevating approved salvaged records to production AI data.
"""

from __future__ import annotations

import json
from typing import Any, Optional
from crewai.tools import tool

from app.core.logging import get_logger
from app.core.exceptions import NotFoundError
from app.repositories.dataset_repository import dataset_repository
from app.repositories.data_repository import data_repository
from app.repositories.processing_job_repository import processing_job_repository
from app.services.ingestion.ingestion_service import ingestion_service
from app.services.validation.validation_service import validation_service
from app.services.cleaning.cleaning_service import cleaning_service
from app.services.preprocessing.preprocessing_service import preprocessing_service
from app.utils.serialization import serialize_document

logger = get_logger(__name__)


# ── Core Backend Implementations (return dict) ──────────────────────

def ingest_dataset_file(
    workspace_id: str,
    product_id: str,
    source_type: str,
    filename: str,
    file_bytes: bytes,
    uploaded_by: str = "system",
) -> dict:
    """
    Ingest customer feedback, reviews, or support tickets from CSV/JSON/Excel.
    Parses content and stores raw data in MongoDB raw_data collection.
    """
    return ingestion_service.ingest_file(
        workspace_id=workspace_id,
        product_id=product_id,
        source_type=source_type,
        filename=filename,
        file_bytes=file_bytes,
        uploaded_by=uploaded_by,
    )


def validate_dataset_records(dataset_id: str, workspace_id: str) -> dict:
    """
    Run Pydantic v2-based schema validation and business rule checks on all raw dataset records.
    """
    return validation_service.validate_dataset(dataset_id=dataset_id, workspace_id=workspace_id)


def clean_and_normalize_dataset(dataset_id: str, workspace_id: str) -> dict:
    """
    Clean and normalize valid records into 'cleaned_data', while quarantining
    and defect-tagging dirty/rejected records in 'dirty_data' MongoDB collection.
    """
    return cleaning_service.clean_dataset(dataset_id=dataset_id, workspace_id=workspace_id)


def preprocess_valid_data(dataset_id: str, workspace_id: str) -> dict:
    """
    Transform valid cleaned data into deep AI-ready ProductSignals with intent tags and keywords.
    Stores output into dedicated 'ai_preprocessed_data' MongoDB collection.
    """
    return preprocessing_service.preprocess_dataset(dataset_id=dataset_id, workspace_id=workspace_id)


def audit_dirty_data(dataset_id: str, workspace_id: str) -> dict:
    """
    Audit quarantined dirty records. Discard pure corrupted noise, identify salvageable
    customer feedback missing metadata, and package candidates for PM review in 'salvaged_data'.
    """
    return preprocessing_service.audit_and_salvage_dirty_data(dataset_id=dataset_id, workspace_id=workspace_id)


def promote_salvaged_data(
    dataset_id: str,
    workspace_id: str,
    salvage_ids: Optional[list[str]] = None,
    reviewer: str = "ProductManager",
) -> dict:
    """
    Promote PM-approved salvaged records from 'salvaged_data' into the primary
    'ai_preprocessed_data' collection for downstream intelligence agents.
    """
    return preprocessing_service.promote_salvaged_records(
        dataset_id=dataset_id,
        workspace_id=workspace_id,
        salvage_ids=salvage_ids,
        reviewer=reviewer,
    )


def get_dataset_usability_report(dataset_id: str) -> dict:
    """
    Get full dataset health report: valid count, dirty count, salvageable count, and AI readiness.
    """
    dataset = dataset_repository.find_by_id(dataset_id)
    if not dataset:
        raise NotFoundError("Dataset", dataset_id)

    raw_cnt = data_repository.count_raw_records(dataset_id)
    cleaned_cnt = data_repository.count_cleaned_records(dataset_id)
    dirty_cnt = data_repository.count_dirty_records(dataset_id)
    ai_preprocessed_cnt = data_repository.count_ai_preprocessed_records(dataset_id)
    salvaged_pending_cnt = data_repository.count_salvaged_records(dataset_id, status="pending_pm_validation")
    salvaged_approved_cnt = data_repository.count_salvaged_records(dataset_id, status="approved")

    total_usable = ai_preprocessed_cnt + salvaged_approved_cnt
    total_evaluated = raw_cnt if raw_cnt > 0 else (cleaned_cnt + dirty_cnt)
    usability_rate = round((total_usable / total_evaluated) * 100, 2) if total_evaluated > 0 else 0.0

    return {
        "dataset_id": dataset_id,
        "filename": dataset.get("filename", ""),
        "source_type": dataset.get("source_type", ""),
        "status": dataset.get("status", ""),
        "counts": {
            "raw_records": raw_cnt,
            "cleaned_valid": cleaned_cnt,
            "quarantined_dirty": dirty_cnt,
            "ai_preprocessed_signals": ai_preprocessed_cnt,
            "salvaged_pending_pm": salvaged_pending_cnt,
            "salvaged_approved": salvaged_approved_cnt,
        },
        "usability_rate_percent": usability_rate,
        "ai_pipeline_status": "ready" if total_usable > 0 else "pending",
    }


def inspect_dataset(dataset_id: str) -> dict:
    """Inspect dataset metadata and stage counts."""
    dataset = dataset_repository.find_by_id(dataset_id)
    if not dataset:
        raise NotFoundError("Dataset", dataset_id)

    result = serialize_document(dataset)
    result["raw_record_count"] = data_repository.count_raw_records(dataset_id)
    result["cleaned_record_count"] = data_repository.count_cleaned_records(dataset_id)
    result["dirty_record_count"] = data_repository.count_dirty_records(dataset_id)
    result["ai_preprocessed_count"] = data_repository.count_ai_preprocessed_records(dataset_id)
    return result


def get_job_status(job_id: str) -> dict:
    """Check progress of a background job."""
    job = processing_job_repository.find_by_id(job_id)
    if not job:
        raise NotFoundError("ProcessingJob", job_id)
    return serialize_document(job)


# ── CrewAI Tool Wrappers ──────────────────────────────────────────

@tool("Validate Dataset Records")
def validate_dataset_records_tool(dataset_id: str, workspace_id: str) -> str:
    """
    Run Pydantic-based schema validation and business rule checks on all records of a dataset.
    Identifies valid records vs defective records and computes data quality scores.
    """
    try:
        res = validate_dataset_records(dataset_id, workspace_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in validate_dataset_records_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Clean and Normalize Dataset")
def clean_and_normalize_dataset_tool(dataset_id: str, workspace_id: str) -> str:
    """
    Clean and normalize valid data records into 'cleaned_data', while simultaneously isolating
    and defect-tagging dirty/rejected records into 'dirty_data' so no raw input is lost.
    """
    try:
        res = clean_and_normalize_dataset(dataset_id, workspace_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in clean_and_normalize_dataset_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Preprocess Valid Data")
def preprocess_valid_data_tool(dataset_id: str, workspace_id: str) -> str:
    """
    Run deep AI preprocessing on valid cleaned records. Extracts linguistic tokens, sentiment clues,
    and intent markers, storing output into dedicated 'ai_preprocessed_data' store for downstream agents.
    """
    try:
        res = preprocess_valid_data(dataset_id, workspace_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in preprocess_valid_data_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Audit Dirty Data")
def audit_dirty_data_tool(dataset_id: str, workspace_id: str) -> str:
    """
    Audit quarantined dirty records. Discard pure corrupted noise, identify salvageable customer feedback
    missing non-critical metadata, and package candidates for Product Manager (PM) review.
    """
    try:
        res = audit_dirty_data(dataset_id, workspace_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in audit_dirty_data_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Promote Salvaged Data")
def promote_salvaged_data_tool(dataset_id: str, workspace_id: str) -> str:
    """
    Promote PM-approved salvaged records from 'salvaged_data' into the main 'ai_preprocessed_data'
    collection with provenance metadata, making them available to downstream intelligence agents.
    """
    try:
        res = promote_salvaged_data(dataset_id, workspace_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in promote_salvaged_data_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Get Dataset Usability Report")
def get_dataset_usability_report_tool(dataset_id: str) -> str:
    """
    Retrieve comprehensive report on dataset health, validity percentage, salvaged records,
    and AI-readiness for downstream agents.
    """
    try:
        res = get_dataset_usability_report(dataset_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in get_dataset_usability_report_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Inspect Dataset")
def inspect_dataset_tool(dataset_id: str) -> str:
    """Inspect dataset metadata and stage counts."""
    try:
        res = inspect_dataset(dataset_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in inspect_dataset_tool: {e}")
        return json.dumps({"error": str(e), "dataset_id": dataset_id})


@tool("Get Job Status")
def get_job_status_tool(job_id: str) -> str:
    """Check progress of a background job."""
    try:
        res = get_job_status(job_id)
        return json.dumps(res, default=str)
    except Exception as e:
        logger.error(f"Error in get_job_status_tool: {e}")
        return json.dumps({"error": str(e), "job_id": job_id})


def get_preprocessing_agent_tools() -> list[Any]:
    """Return all CrewAI tools assigned to the Preprocessing Agent."""
    return [
        validate_dataset_records_tool,
        clean_and_normalize_dataset_tool,
        preprocess_valid_data_tool,
        audit_dirty_data_tool,
        promote_salvaged_data_tool,
        get_dataset_usability_report_tool,
        inspect_dataset_tool,
        get_job_status_tool,
    ]
