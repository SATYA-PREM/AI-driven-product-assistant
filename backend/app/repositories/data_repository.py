from __future__ import annotations

from typing import Any, Optional
from bson import ObjectId
from app.core.database import (
    raw_data_collection,
    cleaned_data_collection,
    processed_data_collection,
    dirty_data_collection,
    ai_preprocessed_collection,
    salvaged_data_collection,
)


class DataRepository:
    """Repository for handling raw, cleaned, dirty, processed, and AI-preprocessed data records."""

    # ── Raw Data ──────────────────────────────────────────────────
    def insert_raw_records(self, records: list[dict]) -> int:
        """Insert multiple raw records."""
        if not records:
            return 0
        result = raw_data_collection.insert_many(records)
        return len(result.inserted_ids)

    def get_raw_records(self, dataset_id: str, skip: int = 0, limit: int = 100) -> list[dict]:
        """Get raw records for a dataset."""
        return list(raw_data_collection.find({"dataset_id": dataset_id}).skip(skip).limit(limit))

    def count_raw_records(self, dataset_id: str) -> int:
        """Count raw records for a dataset."""
        return raw_data_collection.count_documents({"dataset_id": dataset_id})

    # ── Cleaned Data ──────────────────────────────────────────────
    def insert_cleaned_records(self, records: list[dict]) -> int:
        """Insert multiple cleaned records."""
        if not records:
            return 0
        result = cleaned_data_collection.insert_many(records)
        return len(result.inserted_ids)

    def get_cleaned_records(self, dataset_id: str, skip: int = 0, limit: int = 100) -> list[dict]:
        """Get cleaned records for a dataset."""
        return list(cleaned_data_collection.find({"dataset_id": dataset_id}).skip(skip).limit(limit))

    def count_cleaned_records(self, dataset_id: str) -> int:
        """Count cleaned records for a dataset."""
        return cleaned_data_collection.count_documents({"dataset_id": dataset_id})

    # ── Dirty / Rejected Data ─────────────────────────────────────
    def insert_dirty_records(self, records: list[dict]) -> int:
        """Insert records flagged as dirty, corrupted, or rejected during validation."""
        if not records:
            return 0
        result = dirty_data_collection.insert_many(records)
        return len(result.inserted_ids)

    def get_dirty_records(self, dataset_id: str, skip: int = 0, limit: int = 100) -> list[dict]:
        """Get dirty/rejected records for a dataset."""
        return list(dirty_data_collection.find({"dataset_id": dataset_id}).skip(skip).limit(limit))

    def count_dirty_records(self, dataset_id: str) -> int:
        """Count dirty/rejected records for a dataset."""
        return dirty_data_collection.count_documents({"dataset_id": dataset_id})

    # ── Processed Data (Legacy / Standard ProductSignal) ──────────
    def insert_processed_records(self, records: list[dict]) -> int:
        """Insert multiple processed records."""
        if not records:
            return 0
        result = processed_data_collection.insert_many(records)
        return len(result.inserted_ids)

    def get_processed_records(self, dataset_id: str, skip: int = 0, limit: int = 100) -> list[dict]:
        """Get processed records for a dataset."""
        return list(processed_data_collection.find({"dataset_id": dataset_id}).skip(skip).limit(limit))

    def count_processed_records(self, dataset_id: str) -> int:
        """Count processed records for a dataset."""
        return processed_data_collection.count_documents({"dataset_id": dataset_id})

    # ── AI-Preprocessed Data (Deep AI Signals) ─────────────────────
    def insert_ai_preprocessed_records(self, records: list[dict]) -> int:
        """Insert enriched AI-ready signals into dedicated ai_preprocessed_data collection."""
        if not records:
            return 0
        result = ai_preprocessed_collection.insert_many(records)
        return len(result.inserted_ids)

    def get_ai_preprocessed_records(self, dataset_id: str, skip: int = 0, limit: int = 100) -> list[dict]:
        """Get AI-ready signals for a dataset."""
        return list(ai_preprocessed_collection.find({"dataset_id": dataset_id}).skip(skip).limit(limit))

    def count_ai_preprocessed_records(self, dataset_id: str) -> int:
        """Count AI-ready signals for a dataset."""
        return ai_preprocessed_collection.count_documents({"dataset_id": dataset_id})

    # ── Salvaged Data (Pending or Approved by PM) ─────────────────
    def insert_salvaged_records(self, records: list[dict]) -> int:
        """Insert candidates salvaged from dirty data."""
        if not records:
            return 0
        result = salvaged_data_collection.insert_many(records)
        return len(result.inserted_ids)

    def get_salvaged_records(
        self, dataset_id: str, status: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> list[dict]:
        """Get salvaged candidate records for a dataset, optionally filtered by status."""
        query: dict[str, Any] = {"dataset_id": dataset_id}
        if status:
            query["status"] = status
        return list(salvaged_data_collection.find(query).skip(skip).limit(limit))

    def count_salvaged_records(self, dataset_id: str, status: Optional[str] = None) -> int:
        """Count salvaged records for a dataset."""
        query: dict[str, Any] = {"dataset_id": dataset_id}
        if status:
            query["status"] = status
        return salvaged_data_collection.count_documents(query)

    def update_salvaged_status(self, salvage_id: str, status: str, pm_notes: str = "", reviewer: str = "") -> bool:
        """Update review status of a salvaged record."""
        res = salvaged_data_collection.update_one(
            {"salvage_id": salvage_id},
            {"$set": {"status": status, "pm_notes": pm_notes, "reviewed_by": reviewer}}
        )
        return res.modified_count > 0


data_repository = DataRepository()
