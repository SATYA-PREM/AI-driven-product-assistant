from __future__ import annotations
from app.core.constants import SOURCE_TYPE_REQUIRED_FIELDS

def handle_missing_values(records: list[dict], source_type: str) -> list[dict]:
    """
    Handle missing values based on required/optional fields.
    """
    required_fields = SOURCE_TYPE_REQUIRED_FIELDS.get(source_type.upper(), [])
    
    for record in records:
        for field in required_fields:
            if not record.get(field):
                record["_missing_required"] = True
                
        # Optional fields handling could be explicit, but dict.get handles missing by returning None
        for key in list(record.keys()):
            if record[key] == "":
                record[key] = None
                
    return records


class MissingValueHandler:
    def handle_missing_values(self, records: list[dict], source_type: str) -> list[dict]:
        return handle_missing_values(records, source_type)


missing_value_handler = MissingValueHandler()
