"""
header_adapter.py
-------------------
Universal Smart Header Adapter that enables uploading CSV, Excel, and JSON files
with ANY column header names, encodings (including UTF-8 with BOM), or formats.
Automatically maps arbitrary headers to standard Product Intelligence fields.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


def clean_key(key: Any) -> str:
    """Strip BOM, quotes, and whitespace from dictionary keys."""
    if key is None:
        return ""
    s = str(key)
    s = s.lstrip("\ufeff\uffef").strip().strip("\"'").strip()
    return s


def parse_numeric_rating(v: Any) -> int | None:
    """Extract a valid 1-5 integer rating from various formats (e.g. 5, '4.0', '5/5', '1 star')."""
    if v is None or str(v).strip() == "":
        return None
    s = str(v).strip()
    # Check for X/5 pattern
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:/\s*5)?", s)
    if m:
        try:
            val = float(m.group(1))
            val_int = int(round(val))
            return max(1, min(5, val_int))
        except (ValueError, TypeError):
            pass
    return None


def adapt_record_headers(record: dict[str, Any], fallback_idx: int = 1) -> dict[str, Any]:
    """
    Intelligently map arbitrary CSV/Excel column headers to standard product assistant fields:
    - ID: customer_id, feedback_id
    - Text: feedback, feedback_text
    - Rating: rating (1-5)
    - Date: date, feedback_date
    - Dimensions: module, platform, customer_segment, country, source, customer_type, device_or_os, browser_or_client
    """
    if not isinstance(record, dict):
        return {}

    # 1. Clean all keys and normalize string values
    cleaned: dict[str, Any] = {}
    for k, v in record.items():
        ck = clean_key(k)
        if not ck:
            continue
        cleaned[ck] = v.strip() if isinstance(v, str) else v

    result = dict(cleaned)

    # Helper to find value by keyword priority
    def find_by_keywords(keywords: list[str]) -> tuple[str | None, Any]:
        # Exact match first (case-insensitive)
        for kw in keywords:
            for k, v in cleaned.items():
                if k.lower() == kw.lower() and v is not None and str(v).strip() != "":
                    return k, v
        # Substring match next
        for kw in keywords:
            for k, v in cleaned.items():
                if kw.lower() in k.lower() and v is not None and str(v).strip() != "":
                    return k, v
        return None, None

    # 2. Extract or infer ID
    id_keywords = [
        "feedback_id", "customer_id", "review_id", "ticket_id", "id", "user_id",
        "client_id", "account_id", "uuid", "user", "customer", "email", "author"
    ]
    _, found_id = find_by_keywords(id_keywords)
    if found_id is not None and str(found_id).strip() != "":
        resolved_id = str(found_id).strip()
    else:
        resolved_id = f"row_{fallback_idx}"

    result["customer_id"] = resolved_id
    result["feedback_id"] = resolved_id

    # 3. Extract or infer Feedback Text
    text_keywords = [
        "feedback_text", "feedback", "review_text", "review", "description",
        "comment", "comments", "message", "details", "detail", "issue", "problem",
        "complaint", "summary", "note", "notes", "content", "body", "text", "response"
    ]
    _, found_text = find_by_keywords(text_keywords)
    if found_text is not None and str(found_text).strip() != "":
        resolved_text = str(found_text).strip()
    else:
        # Fallback: Find the longest string column in the row
        longest_str = ""
        for k, v in cleaned.items():
            if isinstance(v, str) and len(v.strip()) > len(longest_str) and k not in [
                "feedback_id", "customer_id", "created_at", "date", "feedback_date"
            ]:
                longest_str = v.strip()
        resolved_text = longest_str

    result["feedback"] = resolved_text
    result["feedback_text"] = resolved_text

    # 4. Extract or infer Rating (1-5)
    rating_keywords = ["rating", "score", "stars", "star", "grade", "rank", "rate", "evaluation"]
    _, found_rating = find_by_keywords(rating_keywords)
    parsed_rating = parse_numeric_rating(found_rating)
    if parsed_rating is not None:
        result["rating"] = parsed_rating
    else:
        # If no rating column existed in the CSV, default to 3 (neutral)
        result["rating"] = 3

    # 5. Extract or infer Date
    date_keywords = ["feedback_date", "date", "created_at", "timestamp", "time", "submitted_at", "day"]
    _, found_date = find_by_keywords(date_keywords)
    if found_date is not None and str(found_date).strip() != "":
        resolved_date = str(found_date).strip()
    else:
        resolved_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    result["date"] = resolved_date
    result["feedback_date"] = resolved_date

    # 6. Dimensions (module, platform, customer_segment, country, source, customer_type, browser, device)
    dim_mappings = {
        "module": ["module", "feature", "component", "section", "category", "area"],
        "platform": ["platform", "channel", "app_type", "client_type"],
        "customer_segment": ["customer_segment", "segment", "tier", "plan", "cohort"],
        "country": ["country", "location", "region", "geo", "state"],
        "source": ["source", "origin", "medium", "input_channel"],
        "customer_type": ["customer_type", "user_type", "persona", "role"],
        "browser_or_client": ["browser_or_client", "browser", "client", "agent"],
        "device_or_os": ["device_or_os", "device", "os", "operating_system"],
    }

    for dim_name, kw_list in dim_mappings.items():
        _, val = find_by_keywords(kw_list)
        if val is not None and str(val).strip() != "":
            result[dim_name] = str(val).strip()

    return result

