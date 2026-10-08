"""Public regression tests for the Netflix analytics copilot."""

from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "src"

if str(SOURCE_PATH) not in sys.path:
    sys.path.insert(0, str(SOURCE_PATH))

import copilot_engine
import llm_client


class PublicCopilotTests(unittest.TestCase):

    def test_module_imports(self):
        self.assertTrue(callable(copilot_engine.ask))
        self.assertEqual(
            set(copilot_engine.ANALYTICS_QUERY_REGISTRY.keys()),
            {
                "core_kpis",
                "plan_churn",
                "segment_churn",
                "payment_metrics",
                "engagement_metrics",
                "support_metrics",
                "feedback_metrics",
            },
        )

    def _mock_analytics(self, query_name):
        mock_connection = Mock()
        mock_result = Mock()
        mock_result.df.return_value = pd.DataFrame(
            {"query_name": [query_name]}
        )
        mock_connection.execute.return_value = mock_result

        return mock_connection

    def test_core_kpis(self):
        mock_connection = self._mock_analytics("core_kpis")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
            result = copilot_engine.execute_analytics("core_kpis")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        mock_connection.close.assert_called_once()

    def test_plan_churn(self):
        mock_connection = self._mock_analytics("plan_churn")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
            result = copilot_engine.execute_analytics("plan_churn")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_segment_churn(self):
        mock_connection = self._mock_analytics("segment_churn")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
            result = copilot_engine.execute_analytics("segment_churn")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_payment_metrics(self):
        mock_connection = self._mock_analytics("payment_metrics")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
            result = copilot_engine.execute_analytics("payment_metrics")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_engagement_metrics(self):
        mock_connection = self._mock_analytics("engagement_metrics")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
            result = copilot_engine.execute_analytics("engagement_metrics")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_support_metrics(self):
        mock_connection = self._mock_analytics("support_metrics")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
            result = copilot_engine.execute_analytics("support_metrics")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_feedback_metrics(self):
        mock_connection = self._mock_analytics("feedback_metrics")

        with patch.object(
            copilot_engine,
            "get_connection",
            return_value=mock_connection,
        ):
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
        mock_data = pd.DataFrame(
            {
                "historical_churn_rate_pct": [24.89],
                "customer_count": [8000],
                "churned_customer_count": [1991],
            }
        )

        with patch.object(
            copilot_engine,
            "execute_analytics",
            return_value=mock_data,
        ):
            response = copilot_engine.ask(
                "What is our overall churn rate?"
            )

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
        mock_data = pd.DataFrame(
            {
                "historical_churn_rate_pct": [24.89],
                "customer_count": [8000],
                "churned_customer_count": [1991],
            }
        )

        with patch.object(
            copilot_engine,
            "execute_analytics",
            return_value=mock_data,
        ):
            response = copilot_engine.ask(
                "What is our overall churn rate?"
            )

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["source"], "DuckDB")
        self.assertEqual(
            response["calculation_mode"],
            "deterministic_sql",
        )

    # ============================================================
    # LOCAL LLM TESTS
    # ============================================================

    def test_llm_mode_uses_local_explanation(self):
        mock_data = pd.DataFrame(
            {
                "historical_churn_rate_pct": [24.89],
                "customer_count": [8000],
                "churned_customer_count": [1991],
            }
        )

        llm_answer = (
            "The historical churn rate is 24.89%, meaning "
            "24.89% of customers were classified as churned."
        )

        with patch.object(
            copilot_engine,
            "execute_analytics",
            return_value=mock_data,
        ), patch.object(
            copilot_engine,
            "generate_explanation",
            return_value=llm_answer,
        ) as mock_llm:

            response = copilot_engine.ask(
                "What is our overall churn rate?",
                use_llm=True,
            )

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["intent"], "core_kpis")
        self.assertEqual(response["query_name"], "core_kpis")
        self.assertEqual(response["answer"], llm_answer)

        mock_llm.assert_called_once()

    def test_llm_receives_verified_deterministic_result(self):
        mock_data = pd.DataFrame(
            {
                "historical_churn_rate_pct": [24.89],
                "customer_count": [8000],
                "churned_customer_count": [1991],
            }
        )

        with patch.object(
            copilot_engine,
            "execute_analytics",
            return_value=mock_data,
        ), patch.object(
            copilot_engine,
            "generate_explanation",
            return_value="Verified explanation.",
        ) as mock_llm:

            response = copilot_engine.ask(
                "What is our overall churn rate?",
                use_llm=True,
            )

        mock_llm.assert_called_once()

        question_arg, verified_result_arg = mock_llm.call_args.args

        self.assertEqual(
            question_arg,
            "What is our overall churn rate?",
        )

        self.assertIn("24.89%", verified_result_arg)
        self.assertIn("8,000", verified_result_arg)
        self.assertIn("1,991", verified_result_arg)

        self.assertEqual(
            response["answer"],
            "Verified explanation.",
        )

    def test_llm_failure_falls_back_to_verified_result(self):
        verified_result = (
            "The overall churn rate is 24.89%, based on verified analytics."
        )

        with patch.object(
            llm_client.urllib.request,
            "urlopen",
            side_effect=TimeoutError,
        ):
            result = llm_client.generate_explanation(
                "What is our overall churn rate?",
                verified_result,
            )

        self.assertEqual(result, verified_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)