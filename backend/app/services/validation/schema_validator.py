from __future__ import annotations
from app.core.constants import SOURCE_TYPE_REQUIRED_FIELDS

def validate_schema(record: dict, source_type: str) -> tuple[bool, list[str]]:
    """
    Validate record structure based on source_type.
    """
    errors = []
    required_fields = SOURCE_TYPE_REQUIRED_FIELDS.get(source_type.upper(), [])
    
    for field in required_fields:
        val = record.get(field)
        if val is None or str(val).strip() == "":
            errors.append(f"Missing or empty required field: {field}")
            
    # Check data types if present
    if "rating" in record and record["rating"] is not None:
        try:
            float(record["rating"])
        except ValueError:
            errors.append("Rating must be numeric")
            
    is_valid = len(errors) == 0
    return is_valid, errors


class SchemaValidator:
    def validate_schema(self, record: dict, source_type: str) -> tuple[bool, list[str]]:
        return validate_schema(record, source_type)


schema_validator = SchemaValidator()
