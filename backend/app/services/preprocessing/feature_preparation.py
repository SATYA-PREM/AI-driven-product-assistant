from __future__ import annotations

def prepare_features(record: dict) -> dict:
    """
    Extract basic features from the record.
    """
    features = {}
    text = record.get("text", "")
    
    features["text_length"] = len(text)
    features["word_count"] = len(text.split()) if text else 0
    features["has_rating"] = "rating" in record and record["rating"] is not None
    
    return features
