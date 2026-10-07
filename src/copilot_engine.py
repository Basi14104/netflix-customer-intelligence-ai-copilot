
"""
Netflix Customer Intelligence & AI Analytics Copilot
-----------------------------------------------------

Standalone deterministic analytics engine.

Architecture:
    User Question
        ↓
    Intent Resolution
        ↓
    Approved SQL
        ↓
    DuckDB
        ↓
    Verified Analytics
        ↓
    Business Answer

Design principle:
    DuckDB is the source of truth.
    No LLM is required for deterministic analytics.
"""

from pathlib import Path
import re
import duckdb
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "analytics"
    / "netflix_analytics.duckdb"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """Create a read/write DuckDB connection."""

    return duckdb.connect(str(DATABASE_PATH))


# ============================================================
# APPROVED ANALYTICS QUERIES
# ============================================================

ANALYTICS_QUERY_REGISTRY = {

    "core_kpis": """
        SELECT
            COUNT(*) AS customer_count,
            SUM(CASE WHEN churned = TRUE THEN 1 ELSE 0 END)
                AS churned_customer_count,
            SUM(CASE WHEN churned = FALSE THEN 1 ELSE 0 END)
                AS non_churned_customer_count,
            ROUND(
                100.0 * AVG(CASE WHEN churned = TRUE THEN 1 ELSE 0 END),
                2
            ) AS historical_churn_rate_pct,
            ROUND(AVG(age), 2) AS average_age
        FROM customer_360
    """,

    "plan_churn": """
        SELECT
            latest_plan_id AS plan_id,
            COUNT(*) AS customer_count,
            SUM(CASE WHEN churned = TRUE THEN 1 ELSE 0 END)
                AS churned_customer_count,
            ROUND(
                100.0 * AVG(CASE WHEN churned = TRUE THEN 1 ELSE 0 END),
                2
            ) AS churn_rate_pct
        FROM customer_360
        GROUP BY latest_plan_id
        ORDER BY churn_rate_pct DESC
    """,

    "segment_churn": """
        SELECT
            customer_segment,
            COUNT(*) AS customer_count,
            SUM(CASE WHEN churned = TRUE THEN 1 ELSE 0 END)
                AS churned_customer_count,
            ROUND(
                100.0 * AVG(CASE WHEN churned = TRUE THEN 1 ELSE 0 END),
                2
            ) AS churn_rate_pct
        FROM customer_360
        GROUP BY customer_segment
        ORDER BY churn_rate_pct DESC
    """,

    "payment_metrics": """
        SELECT
            COUNT(*) AS total_payments,
            SUM(
                CASE
                    WHEN payment_status = 'Failed' THEN 1
                    ELSE 0
                END
            ) AS failed_payments,
            ROUND(
                100.0 * AVG(
                    CASE
                        WHEN payment_status = 'Failed' THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS payment_failure_rate_pct,
            ROUND(
                SUM(
                    CASE
                        WHEN payment_status = 'Success'
                        THEN amount
                        ELSE 0
                    END
                ),
                2
            ) AS successful_payment_value
        FROM fact_payment
    """,

    "engagement_metrics": """
        SELECT
            COUNT(*) AS viewing_events,
            COUNT(DISTINCT customer_id) AS customers_with_viewing,
            COUNT(DISTINCT content_id) AS content_items_watched,
            ROUND(
                SUM(watch_duration_minutes) / 60.0,
                2
            ) AS total_watch_hours,
            ROUND(AVG(completion_percentage), 2) AS average_completion_pct,
            ROUND(AVG(session_duration_minutes), 2)
                AS average_session_minutes
        FROM fact_viewing
    """,

    "support_metrics": """
        SELECT
            COUNT(*) AS support_ticket_count,
            COUNT(DISTINCT customer_id) AS customers_with_support,
            SUM(
                CASE
                    WHEN ticket_status = 'Resolved'
                    THEN 1
                    ELSE 0
                END
            ) AS resolved_ticket_count,
            SUM(
                CASE
                    WHEN ticket_status = 'Pending'
                    THEN 1
                    ELSE 0
                END
            ) AS pending_ticket_count,
            SUM(
                CASE
                    WHEN ticket_status = 'Escalated'
                    THEN 1
                    ELSE 0
                END
            ) AS escalated_ticket_count,
            ROUND(
                AVG(resolution_time_hours),
                2
            ) AS average_resolution_hours,
            ROUND(
                AVG(customer_satisfaction_score),
                2
            ) AS average_satisfaction_rating
        FROM fact_support
    """,

    "feedback_metrics": """
        SELECT
            COUNT(*) AS feedback_count,
            COUNT(DISTINCT customer_id)
                AS customers_with_feedback,
            ROUND(AVG(rating), 2) AS average_rating,
            SUM(
                CASE
                    WHEN sentiment_label = 'Negative'
                    THEN 1
                    ELSE 0
                END
            ) AS negative_feedback_count,
            ROUND(
                100.0 * AVG(
                    CASE
                    WHEN sentiment_label = 'Negative'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS negative_feedback_rate_pct
        FROM fact_feedback
    """
}


# ============================================================
# INTENT MAP
# ============================================================

ANALYTICS_INTENT_MAP = {

    "core_kpis": [
        "overall churn",
        "historical churn",
        "churn rate",
        "overall metrics",
        "overall kpis",
        "customer count",
        "how many customers",
        "total customers",
        "number of customers",
        "average age",
        "customer kpis",
    ],

    "plan_churn": [
        "which plan has the highest churn rate",
        "which subscription plan has the highest churn rate",
        "churn by plan",
        "plan churn",
        "churn per plan",
        "which plan",
        "plans and churn",
        "plan level churn",
        "subscription plan churn",
        "churn across plans",
    ],

    "segment_churn": [
        "churn by customer segment",
        "churn by segment",
        "segment churn",
        "customer segment churn",
        "churn per segment",
        "segments and churn",
    ],

    "payment_metrics": [
        "failed payments",
        "payment failures",
        "payment failure rate",
        "payments failed",
        "how many payments failed",
        "failed payment rate",
        "payment metrics",
        "payment performance",
        "successful payments",
        "successful payment value",
        "payment value",
        "payment issues",
    ],

    "engagement_metrics": [
        "watch time",
        "total watch time",
        "how much are customers watching",
        "viewing activity",
        "viewing metrics",
        "engagement metrics",
        "customer engagement",
        "watch hours",
        "total watch hours",
        "average completion",
        "completion rate",
        "session duration",
        "average session",
        "viewing events",
        "content watched",
        "customers with viewing",
    ],

    "support_metrics": [
        "support tickets",
        "support ticket count",
        "how many support tickets",
        "customer support",
        "support metrics",
        "support performance",
        "resolved tickets",
        "pending tickets",
        "escalated tickets",
        "support satisfaction",
    ],

    "feedback_metrics": [
        "customer rating",
        "average rating",
        "customer feedback",
        "feedback metrics",
        "negative feedback",
        "negative feedback rate",
        "feedback sentiment",
        "customer sentiment",
        "ratings",
        "customer reviews",
    ],
}


# ============================================================
# INTENT RESOLUTION
# ============================================================

def normalize_question(question):
    """Normalize user text for deterministic intent matching."""

    return re.sub(
        r"\s+",
        " ",
        question.lower().strip()
    )


def resolve_intent(question):
    """
    Resolve a supported natural-language question
    to an approved analytics query.
    """

    normalized = normalize_question(question)

    matches = []

    for intent, phrases in ANALYTICS_INTENT_MAP.items():

        for phrase in phrases:

            if phrase in normalized:
                matches.append(
                    (len(phrase), intent)
                )

    if not matches:
        return None

    # Prefer the longest matching phrase.
    matches.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return matches[0][1]


# ============================================================
# ANALYTICS EXECUTION
# ============================================================

def execute_analytics(query_name):
    """Execute only a query from the approved registry."""

    if query_name not in ANALYTICS_QUERY_REGISTRY:
        raise ValueError(
            f"Unsupported analytics query: {query_name}"
        )

    con = get_connection()

    try:
        return con.execute(
            ANALYTICS_QUERY_REGISTRY[query_name]
        ).df()

    finally:
        con.close()


# ============================================================
# STRUCTURED RESPONSE
# ============================================================

def build_response(question):
    """Build a deterministic structured analytics response."""

    intent = resolve_intent(question)

    if intent is None:

        return {
            "status": "unsupported",
            "question": question,
            "intent": None,
            "query_name": None,
            "data": None,
            "source": "DuckDB",
            "calculation_mode": "deterministic_sql",
            "message": (
                "I can answer supported Netflix business "
                "analytics questions, but this question is "
                "outside the current analytics scope."
            ),
        }

    data = execute_analytics(intent)

    return {
        "status": "success",
        "question": question,
        "intent": intent,
        "query_name": intent,
        "data": data,
        "source": "DuckDB",
        "calculation_mode": "deterministic_sql",
    }


# ============================================================
# BUSINESS ANSWER FORMATTER
# ============================================================

def format_answer(response):
    """Convert verified analytics into a concise business answer."""

    if response["status"] != "success":
        return response["message"]

    intent = response["intent"]
    data = response["data"]

    if intent == "core_kpis":

        row = data.iloc[0]

        return (
            f"The historical churn rate is "
            f"{row['historical_churn_rate_pct']:.2f}%. "
            f"Out of {int(row['customer_count']):,} customers, "
            f"{int(row['churned_customer_count']):,} are classified "
            f"as churned."
        )

    if intent == "plan_churn":

        parts = []

        for _, row in data.iterrows():

            parts.append(
                f"{row['plan_id']}: "
                f"{row['churn_rate_pct']:.2f}%"
            )

        return "Historical churn by plan: " + "; ".join(parts) + "."

    if intent == "segment_churn":

        parts = []

        for _, row in data.iterrows():

            parts.append(
                f"{row['customer_segment']}: "
                f"{row['churn_rate_pct']:.2f}%"
            )

        return (
            "Historical churn by customer segment: "
            + "; ".join(parts)
            + "."
        )

    if intent == "payment_metrics":

        row = data.iloc[0]

        return (
            f"There were {int(row['total_payments']):,} payments, "
            f"including {int(row['failed_payments']):,} failed "
            f"payments. The payment failure rate was "
            f"{row['payment_failure_rate_pct']:.2f}%."
        )

    if intent == "engagement_metrics":

        row = data.iloc[0]

        return (
            f"Customers generated {row['total_watch_hours']:,.2f} "
            f"watch hours across {int(row['viewing_events']):,} "
            f"viewing events. Average completion was "
            f"{row['average_completion_pct']:.2f}%."
        )

    if intent == "support_metrics":

        row = data.iloc[0]

        return (
            f"There were {int(row['support_ticket_count']):,} "
            f"support tickets. {int(row['resolved_ticket_count']):,} "
            f"were resolved, {int(row['pending_ticket_count']):,} "
            f"were pending, and {int(row['escalated_ticket_count']):,} "
            f"were escalated."
        )

    if intent == "feedback_metrics":

        row = data.iloc[0]

        return (
            f"The average customer rating was "
            f"{row['average_rating']:.2f}. There were "
            f"{int(row['negative_feedback_count']):,} negative "
            f"feedback records, representing "
            f"{row['negative_feedback_rate_pct']:.2f}% of feedback."
        )

    return "Analytics result generated successfully."


# ============================================================
# COPILOT ENTRY POINT
# ============================================================

def ask(question):
    """
    Main Netflix Analytics Copilot entry point.

    Returns verified deterministic business analytics.
    """

    response = build_response(question)

    response["answer"] = format_answer(response)

    return response
