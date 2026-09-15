"""
validator.py
--------------
Validation answers one question per row: "is this row usable?"
It never modifies data -- it only checks it and reports problems.
(Fixing problems is cleaner.py's job, one step later.)

This example validates the ShopEase feedback shape:
    customer_id, rating, feedback, date

If your CSV has different columns, change REQUIRED_FIELDS and the
checks inside validate_row() to match your data -- the pattern
(check required fields -> check types -> check ranges -> return
errors) stays the same for any CSV shape.
"""

REQUIRED_FIELDS = ["customer_id", "rating", "feedback", "date"]
FEEDBACK_CANDIDATE_KEYS = [
    "feedback", "feedback_text", "comment", "comments", "review", 
    "review_text", "text", "customer_feedback", "message", "description", "notes"
]


def detect_feedback_column(row: dict) -> str | None:
    """Finds which key holds the customer feedback text."""
    for key in FEEDBACK_CANDIDATE_KEYS:
        for k in row.keys():
            if k.lower() == key:
                return k
    # Fallback to the longest string field
    longest_k = None
    max_len = 0
    for k, v in row.items():
        if isinstance(v, str) and len(v.strip()) > max_len:
            max_len = len(v.strip())
            longest_k = k
    return longest_k if max_len >= 3 else None


def validate_row(row: dict) -> tuple[bool, list[str]]:
    """
    Checks one row.
    Returns (is_valid, list_of_error_messages).
    Supports both standard ShopEase schema and arbitrary/flexible schemas.
    """
    errors = []

    # If row conforms to standard ShopEase schema (or was intended for it)
    is_standard_schema = any(k in row for k in REQUIRED_FIELDS) and ("customer_id" in row or "rating" in row)

    if is_standard_schema:
        # --- Check 1: required fields must exist and not be empty ---
        for field in REQUIRED_FIELDS:
            value = row.get(field)
            if value is None or str(value).strip() == "":
                errors.append(f"Missing required field: '{field}'")

        if errors:
            return False, errors

        # --- Check 2: rating must be a whole number ---
        try:
            rating = int(row["rating"])
        except (ValueError, TypeError):
            errors.append(f"'rating' must be a whole number, got: '{row.get('rating')}'")
            return False, errors

        # --- Check 3: rating must be in the allowed range (1-5) ---
        if not (1 <= rating <= 5):
            errors.append(f"'rating' must be between 1 and 5, got: {rating}")

        # --- Check 4: feedback text shouldn't be suspiciously short ---
        if len(str(row.get("feedback", "")).strip()) < 3:
            errors.append("'feedback' text is too short to be meaningful")

        return len(errors) == 0, errors

    # Custom / Arbitrary Schema
    feedback_col = detect_feedback_column(row)
    if not feedback_col:
        errors.append("Unable to identify customer feedback text column in row")
        return False, errors

    feedback_val = str(row.get(feedback_col, "")).strip()
    if len(feedback_val) < 3:
        errors.append(f"'{feedback_col}' text is too short to be meaningful")

    # If a rating or score column is present, validate if numeric
    for r_col in ["rating", "score", "stars", "star_rating"]:
        if r_col in row and row[r_col] is not None and str(row[r_col]).strip() != "":
            try:
                r_val = float(row[r_col])
                if r_val < 0 or r_val > 10:
                    errors.append(f"'{r_col}' value out of expected range: {r_val}")
            except (ValueError, TypeError):
                errors.append(f"'{r_col}' must be numeric, got: '{row[r_col]}'")

    return len(errors) == 0, errors


def validate_rows(rows: list[dict]) -> dict:
    """
    Validates every row in the batch and also checks for duplicates
    across rows (a row-vs-row check, which is why it lives here at the
    batch level rather than inside validate_row).

    Returns a summary dict plus the per-row results, e.g.:
        {
            "total": 10, "valid": 8, "invalid": 1, "duplicates": 1,
            "quality_score": 80.0,
            "results": [
                {"row_number": 1, "row": {...}, "is_valid": True, "errors": []},
                {"row_number": 2, "row": {...}, "is_valid": False, "errors": ["..."]},
                ...
            ]
        }
    """
    seen_keys = set()
    results = []
    valid_count = 0
    invalid_count = 0
    duplicate_count = 0

    for i, row in enumerate(rows, start=1):
        # Duplicate check: same customer/user identifier + same feedback text seen before.
        cust_id = row.get("customer_id") or row.get("user_id") or row.get("id") or f"row_{i}"
        fb_col = detect_feedback_column(row)
        fb_val = row.get("feedback") if "feedback" in row else (row.get(fb_col) if fb_col else None)
        dedup_key = (str(cust_id).strip(), str(fb_val).strip() if fb_val else None)

        if dedup_key in seen_keys:
            duplicate_count += 1
            results.append({
                "row_number": i, "row": row, "is_valid": False,
                "errors": ["Duplicate of an earlier row in this file"],
            })
            continue
        seen_keys.add(dedup_key)

        is_valid, errors = validate_row(row)
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1

        results.append({"row_number": i, "row": row, "is_valid": is_valid, "errors": errors})

    total = len(rows)
    quality_score = round((valid_count / total) * 100, 2) if total > 0 else 0.0

    return {
        "total": total,
        "valid": valid_count,
        "invalid": invalid_count,
        "duplicates": duplicate_count,
        "quality_score": quality_score,
        "results": results,
    }
