"""
main.py
---------
FastAPI application for:
1. CSV Upload & Cleaning Pipeline (Milestone 1)
2. Agent 1: Customer Feedback Analysis Agent (Milestone 2)

Run with:
    uvicorn app.main:app --reload
"""

from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.responses import HTMLResponse
from app.config import settings
from app.database import (
    check_connection,
    batches_col,
    raw_data_col,
    cleaned_data_col,
    ai_jobs_col,
    feedback_analyses_col,
)
from app.pipeline import run_pipeline
from app.schemas import SingleAnalysisRequest
from app.agent1 import (
    analyze_single_feedback,
    save_analysis_result,
    run_agent1_for_batch,
)
from app.dashboard import get_dashboard_html
from app.workspace_view import get_workspaces_html

app = FastAPI(
    title="Customer Feedback AI Pipeline",
    description="Milestone 1: CSV Validation & Cleaning | Milestone 2: Agent 1 Feedback Analysis (CrewAI + Gemini)",
    version="2.0.0",
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard_view():
    """Interactive dashboard for uploading CSVs and viewing Agent 1 AI intelligence."""
    return HTMLResponse(content=get_dashboard_html())


@app.get("/workspaces", response_class=HTMLResponse, include_in_schema=False)
def workspaces_view():
    """ProdIntel AI Workspaces Dashboard matching the user's Figma/UI design."""
    return HTMLResponse(content=get_workspaces_html())




@app.get("/health")
def health():
    """Confirms the API is up, MongoDB is reachable, and Gemini API key status."""
    return {
        "api": "ok",
        "mongodb": "ok" if check_connection() else "unreachable",
        "gemini_configured": bool(settings.gemini_api_key),
        "gemini_model": settings.gemini_model,
    }


# =====================================================================
# Milestone 1 Endpoints: CSV Ingestion & Cleaning
# =====================================================================

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a .csv file with standard or custom schema.
    Runs it through the pipeline: parse -> raw_data -> validate -> clean -> cleaned_data.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Please upload a .csv file")

    file_bytes = await file.read()
    summary = run_pipeline(filename=file.filename, file_bytes=file_bytes)
    return summary


@app.get("/batches")
def list_batches():
    """Lists every upload batch, most recent first."""
    batches = list(batches_col.find().sort("uploaded_at", -1))
    for b in batches:
        b["_id"] = str(b["_id"])
    return batches


@app.get("/batches/{batch_id}/raw")
def get_raw_data(batch_id: str):
    """Returns untouched raw rows stored for this batch."""
    docs = list(raw_data_col.find({"batch_id": batch_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


@app.get("/batches/{batch_id}/cleaned")
def get_cleaned_data(batch_id: str):
    """Returns cleaned / AI-ready rows stored for this batch."""
    docs = list(cleaned_data_col.find({"batch_id": batch_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


# =====================================================================
# Milestone 2 Endpoints: Agent 1 Feedback Analysis
# =====================================================================

@app.post("/ai/analyze-record")
def analyze_record(
    payload: SingleAnalysisRequest,
    save_to_db: bool = Query(default=False, description="Whether to store the analysis into MongoDB"),
):
    """
    Directly analyze an individual customer feedback text using Agent 1 (CrewAI + Gemini).
    Returns sentiment, theme, pain point, issue, feature request, intent, product area, keywords, and confidence.
    """
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured in .env. Please configure your API key to run Agent 1.",
        )

    try:
        analysis_result = analyze_single_feedback(
            feedback_text=payload.feedback_text,
            metadata=payload.metadata,
        )

        saved_doc = None
        if save_to_db:
            saved_doc = save_analysis_result(
                batch_id=None,
                record_id=None,
                feedback_text=payload.feedback_text,
                metadata=payload.metadata or {},
                result=analysis_result,
            )

        return {
            "status": "success",
            "feedback_text": payload.feedback_text,
            "analysis": analysis_result.model_dump(),
            "stored_in_db": bool(save_to_db),
            "analysis_id": saved_doc.get("analysis_id") if saved_doc else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 1 analysis failed: {str(e)}")


@app.post("/ai/jobs/analyze/{batch_id}")
def trigger_batch_analysis(
    batch_id: str,
    background_tasks: BackgroundTasks,
    limit: Optional[int] = Query(default=None, description="Max number of records to analyze (useful for testing)"),
    background: bool = Query(default=False, description="If true, runs analysis in background and returns job ID immediately"),
):
    """
    Runs Agent 1 across all cleaned/AI-ready records of a given batch.
    Stores structured analyses into MongoDB 'feedback_analyses' collection.
    """
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured in .env. Please configure your API key to run Agent 1.",
        )

    # Check that batch exists
    batch = batches_col.find_one({"_id": batch_id})
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found.")

    if background:
        # Launch in background
        background_tasks.add_task(run_agent1_for_batch, batch_id=batch_id, limit=limit)
        return {
            "status": "QUEUED",
            "batch_id": batch_id,
            "message": "Agent 1 batch analysis started in the background. Check status at /ai/batches/{batch_id}/analyses or /ai/jobs.",
        }

    try:
        summary = run_agent1_for_batch(batch_id=batch_id, limit=limit)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@app.get("/ai/jobs/{job_id}")
def get_ai_job_status(job_id: str):
    """Retrieves the progress and execution metrics of an AI analysis job."""
    job = ai_jobs_col.find_one({"_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail=f"AI Job {job_id} not found.")
    job["_id"] = str(job["_id"])
    return job


@app.get("/ai/batches/{batch_id}/analyses")
def get_batch_analyses(batch_id: str):
    """Retrieves all Agent 1 analysis results for a given batch from MongoDB."""
    docs = list(feedback_analyses_col.find({"batch_id": batch_id}).sort("created_at", 1))
    for d in docs:
        d["_id"] = str(d["_id"])
    return {
        "batch_id": batch_id,
        "count": len(docs),
        "analyses": docs,
    }


@app.get("/ai/analyses/{analysis_id}")
def get_single_analysis(analysis_id: str):
    """Retrieves a single feedback analysis document by ID."""
    doc = feedback_analyses_col.find_one({"_id": analysis_id})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Analysis record {analysis_id} not found.")
    doc["_id"] = str(doc["_id"])
    return doc
