from __future__ import annotations
from app.utils.date_utils import normalize_date
from app.utils.text_utils import normalize_whitespace

def normalize_record(record: dict, source_type: str) -> dict:
    """
    Normalize specific fields in a record.
    """
    cleaned = record.copy()
    
    if "date" in cleaned and cleaned["date"]:
        cleaned["date"] = normalize_date(str(cleaned["date"]))
        
    if "rating" in cleaned and cleaned["rating"] is not None:
        try:
            cleaned["rating"] = int(float(cleaned["rating"]))
        except ValueError:
            pass
            
    for k, v in cleaned.items():
        if isinstance(v, str):
            cleaned[k] = normalize_whitespace(v).strip()
            
    return cleaned


class Normalizer:
    def normalize_record(self, record: dict, source_type: str) -> dict:
        return normalize_record(record, source_type)


normalizer = Normalizer()
