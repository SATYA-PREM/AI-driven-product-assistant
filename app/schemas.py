"""
schemas.py
-----------
Pydantic data models for Agent 1 (Feedback Analysis Agent),
AI-ready records, and AI job tracking.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class FeedbackAnalysisResult(BaseModel):
    """
    The structured output determined by Gemini via Agent 1 for each
    individual customer feedback record.
    """
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        ...,
        description="Overall sentiment of the feedback: positive, negative, or neutral."
    )
    theme: str = Field(
        ...,
        description="High-level category or subject of the feedback (e.g., Checkout, Authentication, Search, Customer Support, Mobile App, Shipping)."
    )
    pain_point: Optional[str] = Field(
        default=None,
        description="Specific user frustration or difficulty encountered (e.g., 'Payment confirmation is unclear'). Null/None if positive or not applicable."
    )
    issue: Optional[str] = Field(
        default=None,
        description="Specific bug, operational failure, or technical problem (e.g., 'Confirmation screen error'). Null/None if not an issue."
    )
    feature_request: Optional[str] = Field(
        default=None,
        description="New feature, enhancement, or capability requested by the user (e.g., 'Saved searches'). Null/None if not requested."
    )
    intent: Literal["Complaint", "Request", "Praise", "Inquiry", "Feedback"] = Field(
        ...,
        description="Primary intent of the customer: Complaint, Request, Praise, Inquiry, or Feedback."
    )
    product_area: str = Field(
        ...,
        description="Functional product module or area affected (e.g., Checkout, Search, Account, Catalog, Cart, Payment, Notifications)."
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="List of 2 to 5 relevant keywords extracted from the feedback (e.g., ['payment', 'confirmation', 'error'])."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for this classification between 0.0 and 1.0."
    )
    reasoning: Optional[str] = Field(
        default=None,
        description="Brief 1-sentence rationale explaining the classification."
    )


class AIReadyRecord(BaseModel):
    """
    Standardized internal feedback record prepared for AI analysis,
    abstracting away differences in CSV column names.
    """
    record_id: str = Field(..., description="Unique identifier for the record (e.g., cleaned_data document _id or row index).")
    batch_id: Optional[str] = Field(default=None, description="Batch upload identifier.")
    feedback_text: str = Field(..., description="The unclassified customer feedback text.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Associated metadata (rating, date, customer_id, category, source, etc.)."
    )


class SingleAnalysisRequest(BaseModel):
    """Request payload for analyzing a single feedback string directly."""
    feedback_text: str = Field(..., min_length=2, description="The customer feedback text to analyze.")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional extra metadata (e.g., rating, product).")


class StoredAnalysisRecord(BaseModel):
    """Full analysis record saved into MongoDB."""
    analysis_id: str
    batch_id: Optional[str] = None
    record_id: Optional[str] = None
    feedback_text: str
    metadata: Dict[str, Any] = {}
    analysis: FeedbackAnalysisResult
    created_at: datetime


class AIJobResponse(BaseModel):
    """Status and metrics of an AI analysis job."""
    job_id: str
    batch_id: str
    status: Literal["PENDING", "PROCESSING", "COMPLETED", "FAILED"]
    total_records: int
    processed_records: int
    failed_records: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
