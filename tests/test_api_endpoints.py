"""
test_api_endpoints.py
---------------------
Tests FastAPI routes for health, batches, and Agent 1 endpoints.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import FeedbackAnalysisResult


class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["api"], "ok")
        self.assertIn("mongodb", data)
        self.assertIn("gemini_configured", data)

    def test_list_batches_endpoint(self):
        response = self.client.get("/batches")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_ai_job_not_found(self):
        response = self.client.get("/ai/jobs/non_existent_id")
        self.assertEqual(response.status_code, 404)

    @patch("app.main.settings.gemini_api_key", "mock_key")
    @patch("app.main.analyze_single_feedback")
    def test_analyze_record_success_mocked(self, mock_analyze):
        mock_analyze.return_value = FeedbackAnalysisResult(
            sentiment="negative",
            theme="Checkout",
            pain_point="Payment confirmation is unclear",
            issue="Confirmation screen error",
            feature_request="Saved searches",
            intent="Complaint",
            product_area="Checkout",
            keywords=["payment", "confirmation", "error"],
            confidence=0.91,
            reasoning="Customer complained about checkout payment confirmation.",
        )
        response = self.client.post(
            "/ai/analyze-record",
            json={
                "feedback_text": "Payment confirmation is unclear and confirmation screen error occurred during checkout",
                "metadata": {"rating": 2},
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        analysis = data["analysis"]
        self.assertEqual(analysis["sentiment"], "negative")
        self.assertEqual(analysis["theme"], "Checkout")
        self.assertEqual(analysis["pain_point"], "Payment confirmation is unclear")
        self.assertEqual(analysis["issue"], "Confirmation screen error")
        self.assertEqual(analysis["feature_request"], "Saved searches")
        self.assertEqual(analysis["intent"], "Complaint")
        self.assertEqual(analysis["product_area"], "Checkout")
        self.assertEqual(analysis["keywords"], ["payment", "confirmation", "error"])
        self.assertEqual(analysis["confidence"], 0.91)


if __name__ == "__main__":
    unittest.main()
