from datetime import datetime, timezone
from typing import Dict, Any, Optional
import uuid
from app.core.constants import SourceType

class ProcessedDataModel:
    """Model for processed data (ProductSignal) collection."""

    @staticmethod
    def create_document(
        dataset_id: str,
        workspace_id: str,
        product_id: str = "",
        source_type: SourceType | str = "FEEDBACK",
        source_id: str = "",
        text: str = "",
        customer_id: str = "",
        rating: Optional[int] = None,
        date: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        preprocessing_metadata: Optional[Dict[str, Any]] = None,
        canonical_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Create a new processed data document for MongoDB."""
        if canonical_data:
            text = text or canonical_data.get("text", "")
            rating = rating if rating is not None else canonical_data.get("rating")
            date = date or canonical_data.get("date")
            customer_id = customer_id or str(canonical_data.get("customer_id") or "")
            source_id = source_id or str(canonical_data.get("source_id") or "")
            source_type = canonical_data.get("source_type") or source_type
            meta = dict(metadata or {})
            for k in ["module", "platform", "customer_segment", "country", "source", "customer_type", "browser_or_client", "device_or_os"]:
                if canonical_data.get(k):
                    meta[k] = canonical_data.get(k)
            metadata = meta

        st_val = source_type.value if hasattr(source_type, "value") else str(source_type)

        return {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "product_id": product_id,
            "signal_id": str(uuid.uuid4()),
            "source_type": st_val,
            "source_id": source_id,
            "customer_id": customer_id,
            "text": text,
            "rating": rating,
            "date": date,
            "metadata": metadata or {},
            "preprocessing_metadata": preprocessing_metadata or {},
            "canonical_data": canonical_data or {
                "text": text,
                "rating": rating,
                "date": date,
                "customer_id": customer_id,
                "source_id": source_id,
                "source_type": st_val
            },
            "processed_at": datetime.now(timezone.utc)
        }
