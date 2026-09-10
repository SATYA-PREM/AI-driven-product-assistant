from __future__ import annotations
from app.core.constants import SourceType

def validate_business_rules(record: dict, source_type: str) -> tuple[bool, list[str]]:
    """
    Business rule validation per source type.
    """
    errors = []
    source_upper = source_type.upper()
    
    if source_upper == SourceType.FEEDBACK.name:
        if not (record.get("customer_id") or record.get("feedback_id")):
            errors.append("FEEDBACK requires customer_id or feedback_id")
        if not (record.get("feedback") or record.get("feedback_text")):
            errors.append("FEEDBACK requires feedback or feedback_text")
    elif source_upper == SourceType.REVIEW.name:
        if not record.get("review_id"):
            errors.append("REVIEW requires review_id")
        if not record.get("review_text"):
            errors.append("REVIEW requires review_text")
    elif source_upper == SourceType.SUPPORT_TICKET.name:
        if not record.get("ticket_id"):
            errors.append("SUPPORT_TICKET requires ticket_id")
        if not record.get("description"):
            errors.append("SUPPORT_TICKET requires description")
            
    is_valid = len(errors) == 0
    return is_valid, errors


class BusinessRuleValidator:
    def validate_business_rules(self, record: dict, source_type: str) -> tuple[bool, list[str]]:
        return validate_business_rules(record, source_type)


business_rule_validator = BusinessRuleValidator()
