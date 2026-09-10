from __future__ import annotations
from app.models.processed_data import ProcessedDataModel

def canonicalize(record: dict, source_type: str, dataset_id: str, workspace_id: str, product_id: str) -> dict:
    """
    Convert any source type into the canonical format.
    """
    source_upper = source_type.upper()
    
    customer_id = record.get("customer_id")
    rating = record.get("rating")
    date = record.get("date")
    text = record.get("text", "")
    source_id = None
    
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
        "source_type": source_upper
    }
    
    return ProcessedDataModel.create_document(
        dataset_id=dataset_id,
        workspace_id=workspace_id,
        product_id=product_id,
        canonical_data=canonical_data,
        metadata=record.get("features", {})
    )
