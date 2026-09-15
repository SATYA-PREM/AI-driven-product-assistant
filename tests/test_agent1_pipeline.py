"""
test_agent1_pipeline.py
-----------------------
Unit and integration tests for:
1. Pydantic validation of FeedbackAnalysisResult
2. Prompt Manager prompt generation
3. Schema-adaptive feedback extraction
4. Database persistence into MongoDB collections (feedback_analyses, ai_jobs)
"""

import unittest
from datetime import datetime
from pydantic import ValidationError

from app.schemas import FeedbackAnalysisResult, AIReadyRecord, SingleAnalysisRequest
from app.prompts import build_analysis_task_prompt
from app.agent1 import extract_feedback_text_from_doc, save_analysis_result, _clean_json_string
from app.database import feedback_analyses_col, ai_jobs_col


class TestAgent1Pipeline(unittest.TestCase):

    def test_pydantic_validation_success(self):
        """Tests that valid analysis result adheres to the schema."""
        sample_data = {
            "sentiment": "negative",
            "theme": "Checkout",
            "pain_point": "Payment confirmation is unclear",
            "issue": "Confirmation screen error",
            "feature_request": "Saved searches",
            "intent": "Complaint",
            "product_area": "Checkout",
            "keywords": ["payment", "confirmation", "error"],
            "confidence": 0.91,
            "reasoning": "Customer complained about payment confirmation ambiguity."
        }
        result = FeedbackAnalysisResult.model_validate(sample_data)
        self.assertEqual(result.sentiment, "negative")
        self.assertEqual(result.theme, "Checkout")
        self.assertEqual(result.pain_point, "Payment confirmation is unclear")
        self.assertEqual(result.issue, "Confirmation screen error")
        self.assertEqual(result.feature_request, "Saved searches")
        self.assertEqual(result.intent, "Complaint")
        self.assertEqual(result.product_area, "Checkout")
        self.assertEqual(result.keywords, ["payment", "confirmation", "error"])
        self.assertEqual(result.confidence, 0.91)

    def test_pydantic_validation_invalid_sentiment(self):
        """Tests that unexpected sentiment values fail validation."""
        bad_data = {
            "sentiment": "angry",  # Not in Literal["positive", "negative", "neutral"]
            "theme": "Checkout",
            "intent": "Complaint",
            "product_area": "Checkout",
            "confidence": 0.9,
        }
        with self.assertRaises(ValidationError):
            FeedbackAnalysisResult.model_validate(bad_data)

    def test_pydantic_validation_confidence_range(self):
        """Tests that confidence score must be between 0.0 and 1.0."""
        bad_data = {
            "sentiment": "positive",
            "theme": "Support",
            "intent": "Praise",
            "product_area": "Support",
            "confidence": 1.5,  # Out of range
        }
        with self.assertRaises(ValidationError):
            FeedbackAnalysisResult.model_validate(bad_data)

    def test_prompt_manager_generation(self):
        """Tests Prompt Manager dynamic task prompt generation."""
        feedback = "The search results are confusing and irrelevant."
        metadata = {"rating": 2, "customer_id": "C999"}
        prompt = build_analysis_task_prompt(feedback, metadata)
        
        self.assertIn("The search results are confusing and irrelevant.", prompt)
        self.assertIn("C999", prompt)
        self.assertIn("sentiment", prompt)
        self.assertIn("pain_point", prompt)

    def test_adaptive_feedback_extraction(self):
        """Tests adaptive feedback extraction across diverse CSV schemas."""
        # Standard schema
        doc1 = {"data": {"customer_id": "C001", "rating": 2, "feedback": "Slow checkout.", "date": "2026-08-20"}}
        text1, meta1 = extract_feedback_text_from_doc(doc1)
        self.assertEqual(text1, "Slow checkout.")
        self.assertEqual(meta1["customer_id"], "C001")

        # Custom schema: comment column
        doc2 = {"data": {"user": "alice", "score": 5, "comment": "Great experience with mobile app!"}}
        text2, meta2 = extract_feedback_text_from_doc(doc2)
        self.assertEqual(text2, "Great experience with mobile app!")
        self.assertEqual(meta2["user"], "alice")

        # Custom schema: review_text column
        doc3 = {"data": {"id": 101, "review_text": "Shipping arrived three days late.", "carrier": "FedEx"}}
        text3, meta3 = extract_feedback_text_from_doc(doc3)
        self.assertEqual(text3, "Shipping arrived three days late.")
        self.assertEqual(meta3["carrier"], "FedEx")

    def test_clean_json_markdown(self):
        """Tests markdown stripping from JSON strings."""
        raw_md = "```json\n{\"sentiment\": \"positive\", \"theme\": \"Support\"}\n```"
        cleaned = _clean_json_string(raw_md)
        self.assertEqual(cleaned, '{"sentiment": "positive", "theme": "Support"}')

    def test_save_analysis_to_mongodb(self):
        """Tests saving validated analysis result into MongoDB."""
        sample_result = FeedbackAnalysisResult(
            sentiment="negative",
            theme="Checkout",
            pain_point="Payment confirmation is unclear",
            issue="Confirmation screen error",
            feature_request="Saved searches",
            intent="Complaint",
            product_area="Checkout",
            keywords=["payment", "confirmation", "error"],
            confidence=0.91,
            reasoning="Test reasoning.",
        )
        saved = save_analysis_result(
            batch_id="test_batch_123",
            record_id="test_rec_456",
            feedback_text="Payment confirmation is unclear and there is an error.",
            metadata={"rating": 2},
            result=sample_result,
        )
        self.assertIsNotNone(saved.get("_id"))
        self.assertEqual(saved["sentiment"], "negative")
        self.assertEqual(saved["batch_id"], "test_batch_123")
        
        # Verify in MongoDB
        found = feedback_analyses_col.find_one({"_id": saved["_id"]})
        self.assertIsNotNone(found)
        self.assertEqual(found["intent"], "Complaint")

        # Cleanup test document
        feedback_analyses_col.delete_one({"_id": saved["_id"]})


if __name__ == "__main__":
    unittest.main()
