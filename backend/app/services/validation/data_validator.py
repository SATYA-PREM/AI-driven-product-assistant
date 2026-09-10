from __future__ import annotations
from app.utils.date_utils import is_valid_date

def validate_data(record: dict, source_type: str) -> tuple[bool, list[str], list[str]]:
    """
    Validate data quality.
    """
    errors = []
    warnings = []
    
    if "rating" in record and record["rating"] is not None:
        try:
            rating = float(record["rating"])
            if not (1 <= rating <= 5):
                errors.append(f"Rating must be between 1 and 5, got {rating}")
        except ValueError:
            pass # Caught by schema_validator
            
    text_fields = [k for k in record.keys() if "text" in k or k in ["feedback", "description"]]
    for tf in text_fields:
        val = record.get(tf)
        if val and isinstance(val, str):
            if len(val.strip()) < 3:
                warnings.append(f"Text field {tf} is very short")
                
    if "date" in record and record["date"]:
        if not is_valid_date(str(record["date"])):
            errors.append(f"Date {record['date']} is not parseable")
            
    is_valid = len(errors) == 0
    return is_valid, errors, warnings


class DataValidator:
    def validate_data(self, record: dict, source_type: str) -> tuple[bool, list[str], list[str]]:
        return validate_data(record, source_type)


data_validator = DataValidator()
