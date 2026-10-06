"""Public regression tests for the deterministic Netflix analytics copilot."""

from pathlib import Path
import sys
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "src"

if str(SOURCE_PATH) not in sys.path:
    sys.path.insert(0, str(SOURCE_PATH))

import copilot_engine


class PublicCopilotTests(unittest.TestCase):

    def test_module_imports(self):
        self.assertTrue(callable(copilot_engine.ask))
        self.assertTrue(copilot_engine.DATABASE_PATH.exists())

    def test_core_kpis(self):
        result = copilot_engine.execute_analytics("core_kpis")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_plan_churn(self):
        result = copilot_engine.execute_analytics("plan_churn")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_segment_churn(self):
        result = copilot_engine.execute_analytics("segment_churn")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_payment_metrics(self):
        result = copilot_engine.execute_analytics("payment_metrics")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_engagement_metrics(self):
        result = copilot_engine.execute_analytics("engagement_metrics")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_support_metrics(self):
        result = copilot_engine.execute_analytics("support_metrics")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_feedback_metrics(self):
        result = copilot_engine.execute_analytics("feedback_metrics")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_supported_question_routing(self):
        questions = {
            "What is our overall churn rate?": "core_kpis",
            "Show me churn by plan": "plan_churn",
            "What is churn by customer segment?": "segment_churn",
            "How many payments failed?": "payment_metrics",
            "How much are customers watching?": "engagement_metrics",
            "How many support tickets do we have?": "support_metrics",
            "What is the average customer rating?": "feedback_metrics",
        }

        for question, expected_query in questions.items():
            with self.subTest(question=question):
                self.assertEqual(
                    copilot_engine.resolve_intent(question),
                    expected_query,
                )

    def test_supported_question_returns_response(self):
        response = copilot_engine.ask("What is our overall churn rate?")

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["intent"], "core_kpis")
        self.assertEqual(response["query_name"], "core_kpis")
        self.assertIsInstance(response["data"], pd.DataFrame)
        self.assertTrue(response["answer"].strip())

    def test_unsupported_question_is_safe(self):
        response = copilot_engine.ask(
            "Tell me something about Netflix movies"
        )

        self.assertEqual(response["status"], "unsupported")
        self.assertIsNone(response["intent"])
        self.assertIsNone(response["query_name"])

    def test_no_llm_required(self):
        response = copilot_engine.ask("What is our overall churn rate?")

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["source"], "DuckDB")
        self.assertEqual(
            response["calculation_mode"],
            "deterministic_sql",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
