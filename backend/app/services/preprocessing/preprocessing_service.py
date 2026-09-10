"""
preprocessing_service.py
--------------------------
Orchestrates deep AI preprocessing of cleaned valid data into canonical AI-ready ProductSignals,
manages dirty data quarantine audits, and handles Product Manager (PM) salvage promotion.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
import uuid

from app.core.constants import DatasetStatus
from app.core.exceptions import NotFoundError
from app.models.pm_validation import SalvagedDataModel
from app.repositories.data_repository import data_repository
from app.repositories.dataset_repository import dataset_repository
from app.services.preprocessing.canonicalizer import canonicalize
from app.services.preprocessing.feature_preparation import prepare_features
from app.services.preprocessing.structured_preprocessor import preprocess_structured
from app.services.preprocessing.text_preprocessor import preprocess_text


class PreprocessingService:
    """Service orchestrating AI preprocessing, dirty data salvage auditing, and promotion."""

    @staticmethod
    def preprocess_dataset(dataset_id: str, workspace_id: str, user_id: str = "") -> dict:
        """
        Orchestrates transformation of valid cleaned data into deep AI-ready ProductSignals.
        Stores into both 'ai_preprocessed_data' and 'processed_data' collections.
        """
        dataset = dataset_repository.get_by_id(dataset_id)
        if not dataset:
            raise NotFoundError("Dataset", dataset_id)

        source_type = dataset.get("source_type", "feedback")
        product_id = dataset.get("product_id", "")

        cleaned_records = data_repository.get_cleaned_records(dataset_id, limit=50000)
        processed_docs = []
        ai_signal_docs = []

        for rec in cleaned_records:
            row_num = rec.get("row_number", 0)
            data = rec.get("cleaned_record") or rec.get("data") or rec

            # Text preprocessing
            text_val = ""
            for k in ["feedback_text", "feedback", "review_text", "description", "text"]:
                if k in data and data[k]:
                    text_val = preprocess_text(str(data[k]))
                    data[k] = text_val
                    break

            structured = preprocess_structured(data, source_type)
            features = prepare_features(structured)
            structured["features"] = features

            # Canonical processed document
            canonical_doc = canonicalize(
                record=structured,
                source_type=source_type,
                dataset_id=dataset_id,
                workspace_id=workspace_id,
                product_id=product_id,
            )
            canonical_doc["row_number"] = row_num
            processed_docs.append(canonical_doc)

            # Deep AI-ready ProductSignal
            intent = "general_feedback"
            low_text = text_val.lower()
            if any(w in low_text for w in ["bug", "crash", "error", "broken", "issue", "fail", "timed out", "slow"]):
                intent = "bug_report"
            elif any(w in low_text for w in ["would love", "please add", "feature", "suggest", "wish", "easier if"]):
                intent = "feature_request"
            elif any(w in low_text for w in ["love", "great", "excellent", "awesome", "amazing", "useful", "straightforward"]):
                intent = "praise"
            elif any(w in low_text for w in ["cancel", "churn", "refund", "leaving", "terrible", "old address"]):
                intent = "churn_risk"

            ai_signal = {
                "signal_id": str(uuid.uuid4()),
                "dataset_id": dataset_id,
                "workspace_id": workspace_id,
                "product_id": product_id,
                "row_number": row_num,
                "text": text_val,
                "source_type": source_type,
                "intent": intent,
                "features": features,
                "rating": structured.get("rating"),
                "module": data.get("module"),
                "platform": data.get("platform"),
                "customer_segment": data.get("customer_segment"),
                "country": data.get("country"),
                "source": data.get("source"),
                "customer_type": data.get("customer_type"),
                "browser_or_client": data.get("browser_or_client"),
                "device_or_os": data.get("device_or_os"),
                "is_salvaged": False,
                "created_at": datetime.now(timezone.utc),
            }
            # Clean None values
            ai_signal = {k: v for k, v in ai_signal.items() if v is not None}
            ai_signal_docs.append(ai_signal)

        if processed_docs:
            data_repository.insert_processed_records(processed_docs)
        if ai_signal_docs:
            data_repository.insert_ai_preprocessed_records(ai_signal_docs)

        dataset_repository.update_status(dataset_id, DatasetStatus.PREPROCESSED.value)

        return {
            "dataset_id": dataset_id,
            "total_input": len(cleaned_records),
            "processed_count": len(processed_docs),
            "preprocessing_metadata": {
                "pipeline_version": "2.0.0",
                "ai_signals_generated": len(ai_signal_docs),
                "status": "completed",
            },
            "processed_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def get_preprocessing_results(dataset_id: str) -> dict:
        """Retrieve count and metadata for preprocessed signals."""
        ai_cnt = data_repository.count_ai_preprocessed_records(dataset_id)
        proc_cnt = data_repository.count_processed_records(dataset_id)
        total = max(ai_cnt, proc_cnt)
        return {
            "dataset_id": dataset_id,
            "total_input": total,
            "processed_count": total,
            "preprocessing_metadata": {
                "ai_preprocessed_records": ai_cnt,
                "processed_records": proc_cnt,
            },
            "processed_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def audit_and_salvage_dirty_data(dataset_id: str, workspace_id: str) -> dict:
        """
        Audit quarantined dirty records, discard corrupted junk, and extract
        salvageable customer feedback missing non-critical fields for PM review.
        """
        dirty_records = data_repository.get_dirty_records(dataset_id, limit=50000)

        salvaged_docs = []
        corrupted_count = 0

        for r in dirty_records:
            is_salvageable = r.get("is_salvageable", False)
            salvaged_text = r.get("extracted_text", "").strip()

            if is_salvageable and salvaged_text:
                dirty_rec_id = str(r.get("_id", r.get("dirty_record_id", uuid.uuid4())))
                raw_rec = r.get("raw_record", {})
                source_type = raw_rec.get("source_type", "feedback") if isinstance(raw_rec, dict) else "feedback"

                doc = SalvagedDataModel.create_document(
                    dataset_id=dataset_id,
                    workspace_id=workspace_id,
                    dirty_record_id=dirty_rec_id,
                    row_number=r.get("row_number", 0),
                    salvaged_text=salvaged_text,
                    source_type=source_type,
                    inferred_attributes=raw_rec if isinstance(raw_rec, dict) else {},
                    confidence_score=float(r.get("salvage_confidence", 0.8)),
                    status="pending_pm_validation",
                )
                salvaged_docs.append(doc)
            else:
                corrupted_count += 1

        if salvaged_docs:
            data_repository.insert_salvaged_records(salvaged_docs)

        return {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "total_dirty_reviewed": len(dirty_records),
            "salvaged_candidates": len(salvaged_docs),
            "corrupted_discarded": corrupted_count,
            "status": "pending_pm_validation",
            "message": f"Audited {len(dirty_records)} dirty records. {len(salvaged_docs)} candidates staged for PM review.",
        }

    @staticmethod
    def promote_salvaged_records(
        dataset_id: str,
        workspace_id: str,
        salvage_ids: Optional[list[str]] = None,
        reviewer: str = "ProductManager",
    ) -> dict:
        """
        Elevate approved salvaged records from 'salvaged_data' into the main
        'ai_preprocessed_data' and 'processed_data' collections.
        """
        records = data_repository.get_salvaged_records(dataset_id=dataset_id)
        if salvage_ids:
            records = [r for r in records if r.get("salvage_id") in salvage_ids or str(r.get("_id")) in salvage_ids]
        else:
            records = [r for r in records if r.get("status") == "approved"]

        promoted_count = 0
        ai_signal_docs = []
        processed_docs = []

        for rec in records:
            salvage_id = rec.get("salvage_id", str(rec.get("_id", "")))
            text = rec.get("salvaged_text", "")
            source_type = rec.get("source_type", "feedback")
            row_num = rec.get("row_number", 0)

            data_repository.update_salvaged_status(
                salvage_id=salvage_id,
                status="promoted",
                pm_notes="Promoted into production AI signals",
                reviewer=reviewer,
            )

            signal = {
                "signal_id": str(uuid.uuid4()),
                "dataset_id": dataset_id,
                "workspace_id": workspace_id,
                "source_record_id": salvage_id,
                "row_number": row_num,
                "text": text,
                "source_type": source_type,
                "intent": "bug_report" if any(w in text.lower() for w in ["crash", "bug", "error"]) else "salvaged_feedback",
                "is_salvaged": True,
                "metadata": rec.get("inferred_attributes", {}),
                "created_at": datetime.now(timezone.utc),
            }
            ai_signal_docs.append(signal)

            processed_docs.append({
                "dataset_id": dataset_id,
                "workspace_id": workspace_id,
                "product_id": "",
                "canonical_data": {
                    "text": text,
                    "source_type": source_type,
                    "is_salvaged": True,
                },
                "metadata": {"salvage_id": salvage_id},
                "created_at": datetime.now(timezone.utc),
            })
            promoted_count += 1

        if ai_signal_docs:
            data_repository.insert_ai_preprocessed_records(ai_signal_docs)
        if processed_docs:
            data_repository.insert_processed_records(processed_docs)

        return {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "promoted_count": promoted_count,
            "status": "promoted_to_ai_preprocessed",
            "destination_collections": ["ai_preprocessed_data", "processed_data"],
            "message": f"Successfully promoted {promoted_count} salvaged records into active AI signal stream.",
        }

    @staticmethod
    def get_usability_report(dataset_id: str) -> dict:
        """Get dataset health report and usability rate."""
        dataset = dataset_repository.get_by_id(dataset_id)
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


preprocessing_service = PreprocessingService()
