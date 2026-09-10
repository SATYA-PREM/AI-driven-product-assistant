from __future__ import annotations
from app.utils.text_utils import compute_text_hash

def detect_duplicates(records: list[dict], text_field: str = 'feedback') -> list[dict]:
    """
    Detect and mark duplicates in a list of records.
    """
    seen_hashes = {}
    
    for record in records:
        text = str(record.get(text_field) or "")
        text_hash = compute_text_hash(text)
        
        if text_hash in seen_hashes:
            record["is_duplicate"] = True
            record["duplicate_group"] = seen_hashes[text_hash]
        else:
            group_id = str(record.get("_id", "group_" + text_hash[:8]))
            seen_hashes[text_hash] = group_id
            record["is_duplicate"] = False
            record["duplicate_group"] = group_id
            
    return records


class DuplicateHandler:
    def detect_duplicates(self, records: list[dict], text_field: str = 'feedback') -> list[dict]:
        return detect_duplicates(records, text_field)


duplicate_handler = DuplicateHandler()
