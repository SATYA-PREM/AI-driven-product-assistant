"""
Unit tests for CrewAI Preprocessing Agent, Pydantic validation, dirty data quarantine, and PM salvage promotion.
"""

from unittest.mock import MagicMock, patch
from app.agents.preprocessing_agent import (
    preprocessing_agent,
    create_preprocessing_agent,
    create_preprocessing_tasks,
    create_preprocessing_crew,
    get_preprocessing_agent_tools,
)
from app.services.validation.pydantic_validator import pydantic_validator
from app.services.cleaning.cleaning_service import CleaningService
from app.services.preprocessing.preprocessing_service import PreprocessingService


def test_preprocessing_agent_creation():
    agent = create_preprocessing_agent()
    assert agent is not None
    assert "Preprocessing" in agent.role
    assert "ProductSignals" in agent.goal
    assert len(agent.tools) == 8


def test_preprocessing_tools_listing():
    tools = get_preprocessing_agent_tools()
    assert len(tools) == 8
    names = [t.name for t in tools]
    assert "Validate Dataset Records" in names
    assert "Clean and Normalize Dataset" in names
    assert "Preprocess Valid Data" in names
    assert "Audit Dirty Data" in names
    assert "Promote Salvaged Data" in names
    assert "Get Dataset Usability Report" in names


def test_pydantic_validation_feedback_valid():
    valid_data = {
        "customer_id": "C101",
        "rating": 5,
        "feedback": "This product saved us hours of manual work.",
        "date": "2026-09-01",
    }
    is_valid, errors, _ = pydantic_validator.validate_record(valid_data, source_type="feedback")
    assert is_valid is True
    assert len(errors) == 0


def test_pydantic_validation_feedback_invalid_rating():
    invalid_data = {
        "customer_id": "C101",
        "rating": 10,  # Invalid: > 5
        "feedback": "Great tool",
    }
    is_valid, errors, _ = pydantic_validator.validate_record(invalid_data, source_type="feedback")
    assert is_valid is False
    assert any("rating" in err.lower() for err in errors)


def test_pydantic_validation_feedback_missing_required():
    invalid_data = {
        "rating": 4,
        "feedback": "Missing customer id",
    }
    is_valid, errors, _ = pydantic_validator.validate_record(invalid_data, source_type="feedback")
    assert is_valid is False
    assert any("customer_id" in err.lower() for err in errors)


def test_preprocessing_agent_tasks():
    agent = create_preprocessing_agent()
    tasks = create_preprocessing_tasks(agent, "test_ds", "test_ws")
    assert len(tasks) == 4
    assert "test_ds" in tasks[0].description
    assert "test_ds" in tasks[1].description
    assert "test_ds" in tasks[2].description
    assert "test_ds" in tasks[3].description


@patch("app.repositories.dataset_repository.dataset_repository.get_by_id")
@patch("app.repositories.validation_repository.validation_repository.get_by_dataset")
@patch("app.repositories.data_repository.data_repository.get_raw_records")
@patch("app.repositories.data_repository.data_repository.insert_cleaned_records")
@patch("app.repositories.data_repository.data_repository.insert_dirty_records")
@patch("app.repositories.dataset_repository.dataset_repository.update_status")
def test_clean_and_quarantine_dirty_data(
    mock_update_status,
    mock_insert_dirty,
    mock_insert_cleaned,
    mock_get_raw,
    mock_get_val,
    mock_get_ds,
):
    mock_get_ds.return_value = {"_id": "ds1", "source_type": "feedback", "product_id": "p1"}
    mock_get_val.return_value = {
        "record_results": [
            {"row_number": 1, "status": "valid", "errors": []},
            {"row_number": 2, "status": "invalid", "errors": ["Missing required field: customer_id"]},
            {"row_number": 3, "status": "invalid", "errors": ["Missing required field: feedback"]},
        ]
    }
    mock_get_raw.return_value = [
        {"row_number": 1, "feedback": "Great app, highly recommended!", "customer_id": "c1"},
        {"row_number": 2, "feedback": "The app crashes when clicking the billing tab.", "customer_id": ""},
        {"row_number": 3, "feedback": "", "customer_id": "c3"},
    ]
    mock_insert_cleaned.return_value = 1
    mock_insert_dirty.return_value = 2

    res = CleaningService.clean_dataset("ds1", "ws1")

    assert res["cleaned_count"] == 1
    assert res["dirty_count"] == 2
    assert res["salvageable_count"] == 1
    assert res["corrupted_count"] == 1
    assert mock_insert_cleaned.called
    assert mock_insert_dirty.called


@patch("app.repositories.data_repository.data_repository.get_dirty_records")
@patch("app.repositories.data_repository.data_repository.insert_salvaged_records")
@patch("app.repositories.data_repository.data_repository.count_ai_preprocessed_records")
def test_audit_and_salvage_dirty_data(
    mock_count_ai,
    mock_insert_salvaged,
    mock_get_dirty,
):
    mock_get_dirty.return_value = [
        {
            "_id": "d1",
            "row_number": 2,
            "is_salvageable": True,
            "extracted_text": "The app crashes when clicking the billing tab.",
            "raw_record": {"source_type": "feedback", "rating": 1},
            "missing_fields": ["customer_id"],
            "salvage_confidence": 0.85,
        },
        {
            "_id": "d2",
            "row_number": 3,
            "is_salvageable": False,
            "extracted_text": "",
            "raw_record": {},
        },
    ]
    mock_insert_salvaged.return_value = 1
    mock_count_ai.return_value = 10

    report = PreprocessingService.audit_and_salvage_dirty_data("ds1", "ws1")

    assert report["total_dirty_reviewed"] == 2
    assert report["salvaged_candidates"] == 1
    assert report["corrupted_discarded"] == 1
    assert report["status"] == "pending_pm_validation"
    assert mock_insert_salvaged.called


@patch("app.repositories.data_repository.data_repository.get_salvaged_records")
@patch("app.repositories.data_repository.data_repository.update_salvaged_status")
@patch("app.repositories.data_repository.data_repository.insert_ai_preprocessed_records")
@patch("app.repositories.data_repository.data_repository.insert_processed_records")
def test_pm_promotion_of_salvaged_data(
    mock_insert_proc,
    mock_insert_ai,
    mock_update_status,
    mock_get_salvaged,
):
    mock_get_salvaged.return_value = [
        {
            "salvage_id": "salvage_123",
            "row_number": 2,
            "salvaged_text": "The app crashes when clicking the billing tab.",
            "source_type": "feedback",
            "inferred_attributes": {"customer_id": "anonymous_salvaged", "rating": 1},
        }
    ]
    mock_insert_ai.return_value = 1
    mock_insert_proc.return_value = 1

    res = PreprocessingService.promote_salvaged_records("ds1", "ws1", salvage_ids=["salvage_123"])

    assert res["promoted_count"] == 1
    assert res["status"] == "promoted_to_ai_preprocessed"
    assert "ai_preprocessed_data" in res["destination_collections"]
    assert mock_update_status.called
    assert mock_insert_ai.called
