"""
agent1.py
---------
Agent 1 — Feedback Analysis Agent (Milestone 2)

Extracts structured intelligence from individual unclassified customer feedback:
  - Sentiment (positive, negative, neutral)
  - Theme (Checkout, Search, Authentication, etc.)
  - Pain point (specific friction or frustration)
  - Issue (technical error, bug, failure)
  - Feature request (suggested capability)
  - Intent (Complaint, Request, Praise, Inquiry, Feedback)
  - Product area (Checkout, Search, Account, etc.)
  - Keywords (2-5 keywords)
  - Confidence score (0.0 to 1.0)
  - Reasoning

Uses CrewAI with Google Gemini API, validated by Pydantic and persisted in MongoDB.
"""

import os
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

# Opt out of CrewAI telemetry to ensure fast initialization
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from app.config import settings
from app.database import db, batches_col, raw_data_col, cleaned_data_col, ai_jobs_col, feedback_analyses_col
from app.schemas import FeedbackAnalysisResult
from app.prompts import (
    AGENT1_ROLE,
    AGENT1_GOAL,
    AGENT1_BACKSTORY,
    build_analysis_task_prompt,
)


def _clean_json_string(text: str) -> str:
    """Extracts JSON substring if wrapped in markdown code blocks or containing surrounding text."""
    text = text.strip()
    # Remove markdown code blocks if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return text


def create_crewai_agent_and_task(feedback_text: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Initializes CrewAI Agent, Task, and Crew configured for Agent 1.
    """
    from crewai import Agent, Task, Crew, LLM

    # Make sure env vars are populated for LiteLLM / Gemini
    if settings.gemini_api_key:
        os.environ["GEMINI_API_KEY"] = settings.gemini_api_key
        os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

    llm = LLM(
        model=settings.gemini_model,
        api_key=settings.gemini_api_key,
        temperature=0.1,
    )

    agent = Agent(
        role=AGENT1_ROLE,
        goal=AGENT1_GOAL,
        backstory=AGENT1_BACKSTORY,
        llm=llm,
        verbose=False,
    )

    task_description = build_analysis_task_prompt(feedback_text, metadata)

    task = Task(
        description=task_description,
        expected_output="A single valid JSON object containing sentiment, theme, pain_point, issue, feature_request, intent, product_area, keywords, confidence, reasoning.",
        agent=agent,
        output_pydantic=FeedbackAnalysisResult,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    return crew


def analyze_with_direct_gemini(feedback_text: str, metadata: Optional[Dict[str, Any]] = None) -> FeedbackAnalysisResult:
    """
    Direct Gemini API caller via google-genai as a resilient high-performance engine
    or fallback for CrewAI.
    """
    from google import genai
    from google.genai import types

    api_key = settings.gemini_api_key
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

    client = genai.Client(api_key=api_key)
    prompt = build_analysis_task_prompt(feedback_text, metadata)

    model_name = settings.gemini_model.replace("gemini/", "")
    if not model_name:
        model_name = "gemini-1.5-flash"

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FeedbackAnalysisResult,
            temperature=0.1,
        ),
    )

    clean_text = _clean_json_string(response.text)
    return FeedbackAnalysisResult.model_validate_json(clean_text)


def analyze_single_feedback(
    feedback_text: str,
    metadata: Optional[Dict[str, Any]] = None,
    use_crewai: bool = False,
) -> FeedbackAnalysisResult:
    """
    Orchestrates Agent 1 execution:
      1. Uses Google's official Gemini 3.6 Flash API for fast, validated intelligence.
      2. Validates output strictly with Pydantic FeedbackAnalysisResult.
      3. CrewAI agent & crew integration available via use_crewai=True.
    """
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please set GEMINI_API_KEY in your .env file.")

    if not use_crewai:
        return analyze_with_direct_gemini(feedback_text, metadata)

    if use_crewai:
        try:
            crew = create_crewai_agent_and_task(feedback_text, metadata)
            result = crew.kickoff()

            # Check if output is already pydantic object
            if hasattr(result, "pydantic") and result.pydantic:
                if isinstance(result.pydantic, FeedbackAnalysisResult):
                    return result.pydantic
                return FeedbackAnalysisResult.model_validate(result.pydantic.model_dump())

            # Check if output has raw json string
            raw_output = getattr(result, "raw", str(result))
            clean_json = _clean_json_string(raw_output)
            return FeedbackAnalysisResult.model_validate_json(clean_json)
        except Exception as crewai_err:
            # Fallback to direct Gemini API
            print(f"[Agent 1] CrewAI kickoff encountered an error ({crewai_err}), using Gemini direct engine...")
            return analyze_with_direct_gemini(feedback_text, metadata)
    else:
        return analyze_with_direct_gemini(feedback_text, metadata)


def extract_feedback_text_from_doc(doc_data: dict) -> tuple[str, dict]:
    """
    Adaptive extractor: finds the feedback text column across different CSV schemas.
    Common column names: feedback, comment, comments, review, text, description, message, notes.
    """
    data = doc_data.get("data", doc_data)
    
    # Priority list of field names that represent customer feedback
    candidate_keys = [
        "feedback", "feedback_text", "comment", "comments", "review", 
        "review_text", "text", "customer_feedback", "message", "description", "notes"
    ]
    
    feedback_text = ""
    found_key = None
    
    for key in candidate_keys:
        for k in data.keys():
            if k.lower() == key:
                val = data[k]
                if val and str(val).strip():
                    feedback_text = str(val).strip()
                    found_key = k
                    break
        if feedback_text:
            break
            
    # If not found by name, pick the string field with the greatest length (> 5 chars)
    if not feedback_text:
        longest = ""
        longest_key = None
        for k, v in data.items():
            if isinstance(v, str) and len(v.strip()) > len(longest):
                longest = v.strip()
                longest_key = k
        if len(longest) >= 5:
            feedback_text = longest
            found_key = longest_key

    # Remaining fields serve as metadata
    metadata = {k: v for k, v in data.items() if k != found_key}
    return feedback_text, metadata


def save_analysis_result(
    batch_id: Optional[str],
    record_id: Optional[str],
    feedback_text: str,
    metadata: Dict[str, Any],
    result: FeedbackAnalysisResult,
) -> dict:
    """
    Validates and stores the Agent 1 analysis result into MongoDB feedback_analyses collection.
    """
    analysis_id = str(uuid.uuid4())
    doc = {
        "_id": analysis_id,
        "analysis_id": analysis_id,
        "batch_id": batch_id,
        "record_id": record_id,
        "feedback_text": feedback_text,
        "metadata": metadata,
        "sentiment": result.sentiment,
        "theme": result.theme,
        "pain_point": result.pain_point,
        "issue": result.issue,
        "feature_request": result.feature_request,
        "intent": result.intent,
        "product_area": result.product_area,
        "keywords": result.keywords,
        "confidence": result.confidence,
        "reasoning": result.reasoning,
        "agent": "Agent 1 — Feedback Analysis Agent",
        "analysis": result.model_dump(),
        "created_at": datetime.now(timezone.utc),
    }
    feedback_analyses_col.insert_one(doc)
    doc["_id"] = str(doc["_id"])
    return doc


def run_agent1_for_batch(batch_id: str, limit: Optional[int] = None) -> dict:
    """
    Processes all cleaned / AI-ready records of a batch using Agent 1:
      1. Creates an AI job receipt in ai_jobs collection.
      2. Iterates over records in cleaned_data.
      3. Passes each to Agent 1 -> Prompt Manager -> Gemini -> Pydantic validation.
      4. Stores each result into feedback_analyses collection.
      5. Updates job receipt and batch status.
    """
    query = {"batch_id": batch_id}
    cursor = cleaned_data_col.find(query)
    if limit and limit > 0:
        cursor = cursor.limit(limit)
    records = list(cursor)

    if not records:
        # Check raw_data if cleaned_data was empty
        raw_records = list(raw_data_col.find(query))
        if raw_records:
            records = raw_records[:limit] if limit else raw_records

    total_records = len(records)
    job_id = str(uuid.uuid4())

    job_doc = {
        "_id": job_id,
        "job_id": job_id,
        "batch_id": batch_id,
        "agent": "Agent 1 — Feedback Analysis Agent",
        "status": "PROCESSING",
        "total_records": total_records,
        "processed_records": 0,
        "failed_records": 0,
        "errors": [],
        "started_at": datetime.now(timezone.utc),
        "completed_at": None,
    }
    ai_jobs_col.insert_one(job_doc)

    processed_count = 0
    failed_count = 0
    errors = []
    analyses_created = []

    for rec in records:
        rec_id = str(rec.get("_id"))
        feedback_text, metadata = extract_feedback_text_from_doc(rec)

        if not feedback_text:
            failed_count += 1
            err_msg = f"Record {rec_id} has no detectable feedback text."
            errors.append({"record_id": rec_id, "error": err_msg})
            continue

        try:
            analysis_result = analyze_single_feedback(
                feedback_text=feedback_text,
                metadata=metadata,
            )
            saved_doc = save_analysis_result(
                batch_id=batch_id,
                record_id=rec_id,
                feedback_text=feedback_text,
                metadata=metadata,
                result=analysis_result,
            )
            analyses_created.append(saved_doc)
            processed_count += 1
            ai_jobs_col.update_one(
                {"_id": job_id},
                {"$set": {"processed_records": processed_count}},
            )
        except Exception as e:
            failed_count += 1
            err_msg = str(e)
            errors.append({"record_id": rec_id, "error": err_msg})
            ai_jobs_col.update_one(
                {"_id": job_id},
                {
                    "$set": {"failed_records": failed_count},
                    "$push": {"errors": {"record_id": rec_id, "error": err_msg}},
                },
            )

    job_status = "COMPLETED" if failed_count == 0 else ("PARTIAL" if processed_count > 0 else "FAILED")
    completed_at = datetime.now(timezone.utc)

    ai_jobs_col.update_one(
        {"_id": job_id},
        {
            "$set": {
                "status": job_status,
                "processed_records": processed_count,
                "failed_records": failed_count,
                "completed_at": completed_at,
            }
        },
    )

    batches_col.update_one(
        {"_id": batch_id},
        {
            "$set": {
                "ai_status": job_status,
                "ai_analyzed_count": processed_count,
                "last_ai_job_id": job_id,
            }
        },
    )

    return {
        "job_id": job_id,
        "batch_id": batch_id,
        "status": job_status,
        "total_records": total_records,
        "processed_records": processed_count,
        "failed_records": failed_count,
        "errors": errors,
        "analyses": analyses_created,
    }
