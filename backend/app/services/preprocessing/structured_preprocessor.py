from __future__ import annotations

def preprocess_structured(record: dict, source_type: str) -> dict:
    """
    Standardize field names and types.
    """
    processed = record.copy()
    source_upper = source_type.upper()
    
    if source_upper == "REVIEW" and "review_text" in processed:
        processed["text"] = processed.pop("review_text")
    elif source_upper == "SUPPORT_TICKET" and "description" in processed:
        processed["text"] = processed.pop("description")
    elif source_upper == "FEEDBACK" and "feedback" in processed:
        processed["text"] = processed.pop("feedback")
        
    if "rating" in processed and processed["rating"] is not None:
        try:
            processed["rating"] = int(processed["rating"])
        except ValueError:
            pass
            
    return processed
