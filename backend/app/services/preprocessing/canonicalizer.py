from __future__ import annotations
from app.models.processed_data import ProcessedDataModel

def canonicalize(record: dict, source_type: str, dataset_id: str, workspace_id: str, product_id: str) -> dict:
    """
    Convert any source type into the canonical format.
    """
    source_upper = source_type.upper()
    
    customer_id = record.get("customer_id") or record.get("feedback_id")
    rating = record.get("rating")
    date = record.get("feedback_date") or record.get("date") or record.get("created_at")
    text = record.get("feedback_text") or record.get("feedback") or record.get("text", "")
    source_id = record.get("feedback_id")
    
    if source_upper == "REVIEW":
        source_id = record.get("review_id")
    elif source_upper == "SUPPORT_TICKET":
        source_id = record.get("ticket_id")
        
    canonical_data = {
        "text": text,
        "rating": rating,
        "date": date,
        "customer_id": customer_id,
        "source_id": source_id,
        "source_type": source_upper,
        "module": record.get("module"),
        "platform": record.get("platform"),
        "customer_segment": record.get("customer_segment"),
        "country": record.get("country"),
        "source": record.get("source"),
        "customer_type": record.get("customer_type"),
        "browser_or_client": record.get("browser_or_client"),
        "device_or_os": record.get("device_or_os"),
    }
    canonical_data = {k: v for k, v in canonical_data.items() if v is not None}
    
    metadata = dict(record.get("features", {}))
    for k in ["module", "platform", "customer_segment", "country", "source", "customer_type", "browser_or_client", "device_or_os"]:
        if record.get(k):
            metadata[k] = record.get(k)
            
    return ProcessedDataModel.create_document(
        dataset_id=dataset_id,
        workspace_id=workspace_id,
        product_id=product_id,
        canonical_data=canonical_data,
        metadata=metadata
    )
