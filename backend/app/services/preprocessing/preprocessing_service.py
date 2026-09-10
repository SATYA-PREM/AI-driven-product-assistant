"""
preprocessing_service.py
-------------------------
Service for preprocessing cleaned data into canonical AI-ready records,
storing AI-preprocessed signals, auditing dirty/rejected data for salvageable insights,
and promoting PM-validated records into the AI intelligence stream.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import re
import uuid

from app.repositories.data_repository import data_repository
from app.repositories.dataset_repository import dataset_repository
from app.models.pm_validation import SalvagedDataModel
from app.services.preprocessing.text_preprocessor import text_preprocessor
from app.services.preprocessing.structured_preprocessor import structured_preprocessor
from app.services.preprocessing.feature_preparation import feature_preparation
from app.services.preprocessing.canonicalizer import canonicalizer
from app.core.constants import DatasetStatus
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger

logger = get_logger(__name__)


def _extract_ai_understanding(text: str) -> dict[str, Any]:
    """
    Extract linguistic understanding clues, intents, and keywords from raw text.
    Enhances downstream agents' ability to reason without raw LLM re-parsing.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    token_count = len(words)
    char_count = len(text)

    # Intent heuristics
    intents = []
    lower = text.lower()
    if any(w in lower for w in ["bug", "error", "crash", "broken", "failed", "glitch", "freeze"]):
        intents.append("bug_report")
    if any(w in lower for w in ["love", "great", "awesome", "excellent", "best", "perfect", "good"]):
        intents.append("praise")
    if any(w in lower for w in ["wish", "please add", "would be nice", "need", "feature", "suggest"]):
        intents.append("feature_request")
    if any(w in lower for w in ["cancel", "refund", "leaving", "switch to", "unsubscribe", "frustrated"]):
        intents.append("churn_risk")

    # Key terms (words > 4 letters excluding common stops)
    stopwords = {"about", "above", "after", "again", "all", "and", "any", "are", "because", "been", "before", "being", "below", "between", "both", "but", "could", "down", "during", "each", "from", "further", "have", "here", "into", "more", "other", "some", "such", "than", "that", "their", "there", "these", "they", "this", "those", "through", "under", "until", "very", "what", "when", "where", "which", "while", "with", "would"}
    keywords = [w for w in words if len(w) > 4 and w not in stopwords][:10]

    return {
        "token_count": token_count,
        "char_count": char_count,
        "detected_intents": intents,
        "keywords": keywords,
        "signal_clarity": "high" if token_count >= 15 else ("medium" if token_count >= 5 else "low"),
    }


class PreprocessingService:
    """Service for preprocessing cleaned data into canonical AI-ready ProductSignal format."""

    @staticmethod
    def preprocess_dataset(dataset_id: str, workspace_id: str, user_id: str = "") -> dict:
        """
        Orchestrates preprocessing for valid cleaned dataset records:
        1. Preprocesses text and structured attributes.
        2. Enriches with AI understanding (intents, tokens, keywords).
        3. Stores in both standard processed_data and dedicated ai_preprocessed_data collections.
        """
        dataset = dataset_repository.get_by_id(dataset_id)
        if not dataset:
            raise NotFoundError("Dataset", dataset_id)

        source_type = dataset.get("source_type", "feedback")
        product_id = dataset.get("product_id", "")

        cleaned_records = data_repository.get_cleaned_records(dataset_id, limit=50000)
        processed_docs = []
        ai_preprocessed_docs = []

        for record in cleaned_records:
            data = record.get("cleaned_record") or record.get("data") or record

            # Preprocess text fields
            raw_content = ""
            for k in ["feedback", "review_text", "description", "text"]:
                if k in data and data[k]:
                    raw_content = str(data[k])
                    data[k] = text_preprocessor.preprocess_text(data[k])
                    break

            structured = structured_preprocessor.preprocess_structured(data, source_type)
            features = feature_preparation.prepare_features(structured)
            structured["features"] = features

            canonical_doc = canonicalizer.canonicalize(
                record=structured,
                source_type=source_type,
                dataset_id=dataset_id,
                workspace_id=workspace_id,
                product_id=product_id
            )
            processed_docs.append(canonical_doc)

            # Deep AI-enriched document for ai_preprocessed_data collection
            ai_understanding = _extract_ai_understanding(raw_content or canonical_doc.get("text", ""))
            ai_doc = {
                **canonical_doc,
                "ai_signal_id": str(uuid.uuid4()),
                "provenance": "valid_stream",
                "ai_understanding": ai_understanding,
                "ai_preprocessed_at": datetime.now(timezone.utc),
            }
            ai_preprocessed_docs.append(ai_doc)

        if processed_docs:
            data_repository.insert_processed_records(processed_docs)
        if ai_preprocessed_docs:
            data_repository.insert_ai_preprocessed_records(ai_preprocessed_docs)

        dataset_repository.update_status(
            dataset_id,
            DatasetStatus.READY.value,
            extra_fields={"updated_at": datetime.now(timezone.utc)}
        )

        return {
            "dataset_id": dataset_id,
            "total_input": len(cleaned_records),
            "processed_count": len(processed_docs),
            "ai_preprocessed_count": len(ai_preprocessed_docs),
            "preprocessing_metadata": {
                "canonical_format": "ProductSignal",
                "features_extracted": True,
                "ai_understanding_enriched": True,
            },
            "processed_at": datetime.now(timezone.utc)
        }

    @staticmethod
    def audit_and_salvage_dirty_data(dataset_id: str, workspace_id: str) -> dict:
        """
        Audits dirty/rejected data for recoverable feedback records where some parts were missing.
        Saves salvageable candidates into salvaged_data collection with status 'pending_pm_validation',
        and generates a dataset usability report.
        """
        dirty_records = data_repository.get_dirty_records(dataset_id, limit=5000)
        total_dirty = len(dirty_records)
        corrupted_count = 0
        candidate_docs = []

        for rec in dirty_records:
            if not rec.get("is_salvageable", False):
                corrupted_count += 1
                continue

            raw = rec.get("raw_record", {})
            text = rec.get("extracted_text", "")
            if not text:
                corrupted_count += 1
                continue

            candidate = SalvagedDataModel.create_document(
                dataset_id=dataset_id,
                workspace_id=workspace_id,
                dirty_record_id=str(rec.get("_id", "")),
                row_number=rec.get("row_number", 0),
                salvaged_text=text,
                source_type=raw.get("source_type", "feedback"),
                inferred_attributes={
                    "customer_id": raw.get("customer_id") or raw.get("user_id") or "anonymous_salvaged",
                    "rating": raw.get("rating"),
                    "date": raw.get("date") or datetime.now(timezone.utc).isoformat(),
                    "missing_fields": rec.get("missing_fields", []),
                },
                confidence_score=rec.get("salvage_confidence", 0.8),
                status="pending_pm_validation",
                pm_notes="Auto-flagged by Preprocessing Agent: substantive customer feedback preserved",
            )
            candidate_docs.append(candidate)

        if candidate_docs:
            data_repository.insert_salvaged_records(candidate_docs)

        valid_count = data_repository.count_ai_preprocessed_records(dataset_id)
        usability_score = (
            round(((valid_count + len(candidate_docs)) / (valid_count + total_dirty)) * 100, 2)
            if (valid_count + total_dirty) > 0 else 100.0
        )

        return {
            "dataset_id": dataset_id,
            "total_dirty_reviewed": total_dirty,
            "corrupted_discarded": corrupted_count,
            "salvaged_candidates": len(candidate_docs),
            "status": "pending_pm_validation",
            "usability_score": usability_score,
            "recommendation": (
                "Dataset has high salvage potential. Review candidate records in salvaged_data collection."
                if len(candidate_docs) > 0 else "Dirty records contain only corrupted noise; safe to proceed with valid data."
            ),
        }

    @staticmethod
    def promote_salvaged_records(
        dataset_id: str,
        workspace_id: str,
        salvage_ids: Optional[list[str]] = None,
        reviewer: str = "ProductManager",
    ) -> dict:
        """
        Promotes PM-validated salvaged records into the primary ai_preprocessed_data collection.
        After PM review, these records are elevated to production AI signals for downstream agents.
        """
        query_status = "approved" if not salvage_ids else None
        candidates = data_repository.get_salvaged_records(dataset_id, status=query_status, limit=1000)

        # If specific salvage_ids were approved in this request:
        if salvage_ids:
            candidates = [c for c in candidates if c.get("salvage_id") in salvage_ids]
            for c in candidates:
                data_repository.update_salvaged_status(
                    c["salvage_id"], status="approved", reviewer=reviewer
                )

        if not candidates:
            # Fallback: if there are pending candidates and PM requests promotion of all available candidates
            all_pending = data_repository.get_salvaged_records(dataset_id, status="pending_pm_validation", limit=1000)
            candidates = all_pending
            for c in candidates:
                data_repository.update_salvaged_status(
                    c["salvage_id"], status="approved", pm_notes="Batch approved by PM", reviewer=reviewer
                )

        promoted_docs = []
        for cand in candidates:
            text = cand.get("salvaged_text", "")
            inferred = cand.get("inferred_attributes", {})
            ai_understanding = _extract_ai_understanding(text)

            signal_doc = {
                "dataset_id": dataset_id,
                "workspace_id": workspace_id,
                "signal_id": str(uuid.uuid4()),
                "ai_signal_id": str(uuid.uuid4()),
                "source_type": cand.get("source_type", "feedback"),
                "source_id": f"salvaged_row_{cand.get('row_number')}",
                "customer_id": inferred.get("customer_id", "anonymous_salvaged"),
                "text": text,
                "rating": inferred.get("rating"),
                "date": inferred.get("date"),
                "provenance": "pm_approved_salvage",
                "ai_understanding": ai_understanding,
                "metadata": {"salvage_id": cand.get("salvage_id"), "approved_by": reviewer},
                "processed_at": datetime.now(timezone.utc),
            }
            promoted_docs.append(signal_doc)

        if promoted_docs:
            data_repository.insert_ai_preprocessed_records(promoted_docs)
            data_repository.insert_processed_records(promoted_docs)

        return {
            "dataset_id": dataset_id,
            "promoted_count": len(promoted_docs),
            "status": "promoted_to_ai_preprocessed",
            "destination_collections": ["ai_preprocessed_data", "processed_data"],
            "reviewed_by": reviewer,
        }

    @staticmethod
    def get_preprocessing_results(dataset_id: str) -> dict:
        """Get summary of processed signals and AI readiness for a dataset."""
        standard_count = data_repository.count_processed_records(dataset_id)
        ai_count = data_repository.count_ai_preprocessed_records(dataset_id)
        salvaged_count = data_repository.count_salvaged_records(dataset_id)
        dirty_count = data_repository.count_dirty_records(dataset_id)

        return {
            "dataset_id": dataset_id,
            "total_ai_signals": ai_count or standard_count,
            "standard_signals": standard_count,
            "salvaged_candidates": salvaged_count,
            "dirty_records": dirty_count,
            "status": "ready_for_agents" if (ai_count or standard_count) > 0 else "pending",
            "processed_at": datetime.now(timezone.utc)
        }


preprocessing_service = PreprocessingService()
