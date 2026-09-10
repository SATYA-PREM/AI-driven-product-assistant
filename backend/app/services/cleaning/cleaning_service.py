from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from app.repositories.data_repository import data_repository
from app.repositories.validation_repository import validation_repository
from app.repositories.dataset_repository import dataset_repository
from app.models.cleaned_data import CleanedDataModel
from app.models.dirty_data import DirtyDataModel
from app.services.cleaning.duplicate_handler import duplicate_handler
from app.services.cleaning.missing_value_handler import missing_value_handler
from app.services.cleaning.normalization import normalizer
from app.core.constants import DatasetStatus
from app.core.exceptions import NotFoundError


class CleaningService:
    """Service for cleaning, normalizing valid records, and quarantining dirty/rejected data."""

    @staticmethod
    def clean_dataset(dataset_id: str, workspace_id: str, user_id: str = "") -> dict:
        """
        Orchestrates the cleaning pipeline:
        1. Validates & normalizes clean data records -> stores in cleaned_data.
        2. Categorizes dirty/rejected records (corrupted vs missing fields) -> stores in dirty_data.
        """
        dataset = dataset_repository.get_by_id(dataset_id)
        if not dataset:
            raise NotFoundError("Dataset", dataset_id)

        source_type = dataset.get("source_type", "feedback")
        product_id = dataset.get("product_id", "")

        val_summary = validation_repository.get_by_dataset(dataset_id)
        valid_row_numbers = set()
        validation_map: dict[int, Any] = {}
        if val_summary and "record_results" in val_summary:
            for r in val_summary["record_results"]:
                row_no = r.get("row_number")
                validation_map[row_no] = r
                if r.get("status") in ["valid", "warning"]:
                    valid_row_numbers.add(row_no)

        raw_records = data_repository.get_raw_records(dataset_id, limit=50000)

        # ── 1. Process Valid Records ─────────────────────────────────
        if valid_row_numbers:
            valid_raw_records = [r for r in raw_records if r.get("row_number") in valid_row_numbers]
            invalid_raw_records = [r for r in raw_records if r.get("row_number") not in valid_row_numbers]
        else:
            valid_raw_records = raw_records
            invalid_raw_records = []

        data_list = [r.get("original_record") or r.get("data") or r for r in valid_raw_records]

        text_field = "feedback"
        if source_type.lower() == "review":
            text_field = "review_text"
        elif source_type.lower() == "support_ticket":
            text_field = "description"

        data_list = duplicate_handler.detect_duplicates(data_list, text_field)
        data_list = missing_value_handler.handle_missing_values(data_list, source_type)

        cleaned_docs = []
        dup_count = 0

        for raw_rec, data in zip(valid_raw_records, data_list):
            is_dup = data.get("is_duplicate", False)
            if is_dup:
                dup_count += 1

            cleaned_record = normalizer.normalize_record(data, source_type)
            doc = CleanedDataModel.create_document(
                dataset_id=dataset_id,
                workspace_id=workspace_id,
                product_id=product_id,
                source_record_id=str(raw_rec.get("source_record_id", "")),
                row_number=raw_rec.get("row_number", 0),
                cleaned_record=cleaned_record,
                is_duplicate=is_dup,
                duplicate_group=data.get("duplicate_group", "")
            )
            cleaned_docs.append(doc)

        if cleaned_docs:
            data_repository.insert_cleaned_records(cleaned_docs)

        # ── 2. Quarantine & Analyze Dirty / Invalid Records ───────────
        dirty_docs = []
        salvageable_count = 0
        corrupted_count = 0

        for raw_rec in invalid_raw_records:
            row_no = raw_rec.get("row_number", 0)
            val_info = validation_map.get(row_no, {})
            errors = val_info.get("errors", [])
            data = raw_rec.get("original_record") or raw_rec.get("data") or raw_rec

            raw_text = str(
                data.get("feedback")
                or data.get("review_text")
                or data.get("description")
                or data.get("text")
                or ""
            ).strip()

            missing_fields = [
                e.replace("Missing required field: ", "")
                for e in errors
                if "Missing required field:" in e
            ]
            is_corrupt = len(raw_text) == 0 or raw_text.lower() in ["nan", "null", "none", "n/a", "undefined"]
            is_dup = any("Duplicate" in e for e in errors)

            if is_corrupt:
                defect_type = "corrupted"
                is_salvageable = False
                salvage_reason = "Unusable or empty text content"
                confidence = 0.0
                corrupted_count += 1
            elif is_dup:
                defect_type = "duplicate"
                is_salvageable = False
                salvage_reason = "Identical duplicate text"
                confidence = 0.0
            elif missing_fields and len(raw_text) >= 10:
                defect_type = "missing_fields"
                is_salvageable = True
                salvage_reason = f"Contains substantive feedback ({len(raw_text)} chars) despite missing metadata"
                confidence = 0.85
                salvageable_count += 1
            else:
                defect_type = "schema_defect"
                is_salvageable = len(raw_text) >= 10
                salvage_reason = "Potential signal requiring PM verification" if is_salvageable else "Low signal noise"
                confidence = 0.6 if is_salvageable else 0.1
                if is_salvageable:
                    salvageable_count += 1
                else:
                    corrupted_count += 1

            dirty_doc = DirtyDataModel.create_document(
                dataset_id=dataset_id,
                workspace_id=workspace_id,
                row_number=row_no,
                raw_record=data,
                validation_errors=errors,
                defect_type=defect_type,
                missing_fields=missing_fields,
                extracted_text=raw_text,
                is_salvageable=is_salvageable,
                salvage_reason=salvage_reason,
                salvage_confidence=confidence,
            )
            dirty_docs.append(dirty_doc)

        if dirty_docs:
            data_repository.insert_dirty_records(dirty_docs)

        dataset_repository.update_status(
            dataset_id,
            DatasetStatus.CLEANED.value,
            extra_fields={"updated_at": datetime.now(timezone.utc)}
        )

        return {
            "dataset_id": dataset_id,
            "total_input": len(raw_records),
            "cleaned_count": len(cleaned_docs),
            "duplicate_count": dup_count,
            "dirty_count": len(dirty_docs),
            "salvageable_count": salvageable_count,
            "corrupted_count": corrupted_count,
            "cleaning_metadata": {
                "rules_applied": [
                    "text_normalization",
                    "date_normalization",
                    "deduplication",
                    "missing_value_imputation",
                    "dirty_data_quarantine",
                ]
            },
            "cleaned_at": datetime.now(timezone.utc)
        }

    @staticmethod
    def get_cleaning_results(dataset_id: str) -> dict:
        """Get cleaning summary for a dataset."""
        cleaned_cnt = data_repository.count_cleaned_records(dataset_id)
        dirty_cnt = data_repository.count_dirty_records(dataset_id)
        return {
            "dataset_id": dataset_id,
            "total_input": cleaned_cnt + dirty_cnt,
            "cleaned_count": cleaned_cnt,
            "dirty_count": dirty_cnt,
            "duplicate_count": 0,
            "cleaning_metadata": {},
            "cleaned_at": datetime.now(timezone.utc)
        }


cleaning_service = CleaningService()
