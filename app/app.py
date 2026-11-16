import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# PROJECT PATHS AND ENGINE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "src"

if str(SOURCE_PATH) not in sys.path:
    sys.path.insert(0, str(SOURCE_PATH))

from copilot_engine import ask


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Intelligence | Analytics Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --surface: #17191f;
        --surface-2: #20232b;
        --border: rgba(255,255,255,.09);
        --muted: #a7adba;
        --accent: #e50914;
        --success: #45c486;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 0%, rgba(229,9,20,.10), transparent 28%),
            #0e1015;
    }

    [data-testid="stSidebar"] {
        background: #17191f;
        border-right: 1px solid var(--border);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .hero {
        padding: 2.1rem 2.2rem;
        border: 1px solid var(--border);
        border-radius: 20px;
        background: linear-gradient(120deg, #1c1f27 0%, #14161c 65%, #251316 100%);
        margin-bottom: 1.4rem;
    }

    .eyebrow {
        color: #ff737b;
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .65rem;
    }

    .hero h1 {
        font-size: clamp(1.8rem, 3vw, 2.65rem);
        line-height: 1.15;
        margin: 0 0 .7rem 0;
        font-weight: 780;
    }

    .hero p {
        color: #c1c5ce;
        font-size: 1.02rem;
        margin: 0;
        max-width: 850px;
    }

    .section-kicker {
        color: #ff737b;
        text-transform: uppercase;
        font-size: .72rem;
        letter-spacing: .13em;
        font-weight: 750;
        margin-bottom: .35rem;
    }

    .muted {
        color: var(--muted);
    }

    .info-card {
        background: linear-gradient(145deg, #1b1e26, #15171d);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        min-height: 112px;
    }

    .info-label {
        color: #aeb4c0;
        font-size: .83rem;
        margin-bottom: .5rem;
    }

    .info-value {
        color: #ffffff;
        font-size: 1.85rem;
        line-height: 1.15;
        font-weight: 780;
    }

    .info-note {
        color: #89919f;
        font-size: .75rem;
        margin-top: .4rem;
    }

    .trust-box {
        border: 1px solid rgba(69,196,134,.25);
        background: rgba(69,196,134,.08);
        border-radius: 13px;
        padding: .9rem 1rem;
        color: #c8f2dc;
    }

    .answer-panel {
        background: #191c23;
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
    }

    div[data-testid="stMetric"] {
        background: #191c23;
        border: 1px solid var(--border);
        padding: 1rem;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #b1b7c2;
    }

    .footer {
        color: #828a98;
        font-size: .78rem;
        text-align: center;
        padding-top: 1rem;
    }

    div.stButton > button[kind="primary"] {
        background: #e50914;
        border: 1px solid #e50914;
        color: white;
        border-radius: 10px;
        font-weight: 650;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #bd0811;
        border-color: #bd0811;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONSTANTS
# ============================================================

EXAMPLE_QUESTIONS = [
    "What is our overall churn rate?",
    "Which subscription plan has the highest churn rate?",
    "Which customer segment has the highest churn?",
    "What is the payment failure rate?",
    "How much are customers watching?",
    "How many support tickets do we have?",
    "What is the average customer rating?",
]

ANALYTICS_QUESTIONS = {
    "Subscription churn": "Which subscription plan has the highest churn rate?",
    "Customer segments": "Which customer segment has the highest churn?",
    "Payments": "What is the payment failure rate?",
    "Engagement": "How much are customers watching?",
    "Customer support": "How many support tickets do we have?",
    "Customer feedback": "What is the average customer rating?",
}


# ============================================================
# HELPERS
# ============================================================

def run_question(question: str, use_llm: bool = False) -> dict:
    """Run a question through the existing deterministic copilot engine."""
    try:
        result = ask(question.strip(), use_llm=use_llm)
        if not isinstance(result, dict):
            return {
                "status": "error",
                "answer": "The analytics engine returned an unexpected response.",
            }
        return result
    except Exception as exc:
        return {
            "status": "error",
            "answer": "The request could not be completed. Check that the local "
                      "DuckDB analytics database is available, then try again.",
            "technical_error": str(exc),
        }


def display_result_table(result: dict, key_prefix: str) -> None:
    data = result.get("data")
    if data is None:
        st.info("No tabular analytics were returned for this question.")
        return

    if isinstance(data, pd.DataFrame):
        frame = data.copy()
    else:
        try:
            frame = pd.DataFrame(data)
        except Exception:
            st.info("The result is available, but it could not be displayed as a table.")
            return

    if frame.empty:
        st.info("The analytics query returned no rows.")
        return

    st.dataframe(frame, use_container_width=True, hide_index=True)

    # Allow users to export the exact verified result returned by the engine.
    csv_data = frame.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download verified results (CSV)",
        data=csv_data,
        file_name="verified_analytics_results.csv",
        mime="text/csv",
        key=f"{key_prefix}_download_verified_analytics",
    )

    numeric_columns = frame.select_dtypes(include="number").columns.tolist()
    categorical_columns = [
        col for col in frame.columns if col not in numeric_columns
    ]

    # A single aggregate row has no meaningful category axis. Avoid plotting
    # unrelated measures (counts, percentages and averages) on one scale.
    if len(frame) < 2 or not categorical_columns or not numeric_columns:
        st.caption(
            "A comparison chart is shown when the result contains multiple "
            "categories. This result is best interpreted from the verified table."
        )
        return

    preferred_metrics = [
        col for col in numeric_columns
        if any(token in col.lower() for token in (
            "churn_rate", "failure_rate", "completion", "satisfaction",
            "rating", "percentage", "rate_pct"
        ))
    ]
    default_metric = preferred_metrics[0] if preferred_metrics else numeric_columns[0]

    with st.expander("Explore chart", expanded=True):
        metric_column = st.selectbox(
            "Choose a metric to compare",
            options=numeric_columns,
            index=numeric_columns.index(default_metric),
            key=f"{key_prefix}_analytics_chart_metric",
        )

        chart_frame = frame[[categorical_columns[0], metric_column]].copy()
        chart_frame[metric_column] = pd.to_numeric(
            chart_frame[metric_column], errors="coerce"
        )
        chart_frame = chart_frame.dropna(subset=[metric_column])

        if not chart_frame.empty:
            chart_frame = chart_frame.set_index(categorical_columns[0])
            st.bar_chart(chart_frame, y=metric_column)
        else:
            st.info("No numeric values are available for this chart.")


def display_verification(result: dict) -> None:
    st.markdown("#### Verification details")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.caption("Detected intent")
        st.code(str(result.get("intent", "N/A")), language=None)

    with c2:
        st.caption("Analytics query")
        st.code(str(result.get("query_name", "N/A")), language=None)

    with c3:
        st.caption("Source")
        st.code(str(result.get("source", "N/A")), language=None)

    st.caption(
        f"Calculation mode: `{result.get('calculation_mode', 'deterministic_sql')}`"
    )


def show_copilot_result(result: dict) -> None:
    status = result.get("status")

    if status == "unsupported":
        st.warning(
            "This question is outside the currently supported Netflix business "
            "analytics scope. Try one of the example questions."
        )
        return

    if status == "error":
        st.error(result.get("answer", "Something went wrong."))
        if result.get("technical_error"):
            with st.expander("Technical details"):
                st.code(result["technical_error"])
        return

    st.markdown("### Copilot answer")
    with st.container(border=True):
        # Render as Markdown instead of injecting the answer into raw HTML.
        # This correctly displays bold text, lists, and other Markdown formatting.
        st.markdown(result.get("answer", "No answer generated."))

    display_verification(result)

    st.markdown("#### Verified analytics")
    display_result_table(result, key_prefix="copilot")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 📊 Netflix Intelligence")
    st.caption("CUSTOMER ANALYTICS PLATFORM")
    st.divider()

    st.markdown("### Explore")
    st.markdown(
        """
        - Executive overview
        - Customer and churn analytics
        - Subscription and payment analytics
        - Engagement and support analytics
        - AI analytics copilot
        """
    )

    st.divider()
    st.markdown("### 🔐 Data grounding")
    st.markdown(
        """
        <div class="trust-box">
            <b>Verified analytics first</b><br>
            Numerical results come from the deterministic DuckDB analytics layer.
            The AI layer explains those results; it does not invent metrics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### 💡 Try a question")
    for index, example in enumerate(EXAMPLE_QUESTIONS):
        if st.button(
            example,
            key=f"sidebar_example_{index}",
            use_container_width=True,
        ):
            st.session_state["selected_question"] = example
            st.session_state["run_selected_question"] = True


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Customer intelligence • Business analytics • AI</div>
        <h1>Netflix Customer Intelligence<br> &amp; AI Analytics Copilot</h1>
        <p>
            Explore customer behaviour, understand churn, monitor business
            performance and ask questions in natural language — with answers
            grounded in verified analytics.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOP-LEVEL NAVIGATION
# ============================================================

overview_tab, copilot_tab, explorer_tab, methodology_tab = st.tabs(
    ["Executive overview", "AI copilot", "Analytics explorer", "Methodology"]
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

with overview_tab:
    st.markdown('<div class="section-kicker">Business snapshot</div>', unsafe_allow_html=True)
    st.subheader("Executive overview")
    st.markdown(
        '<p class="muted">A high-level view of the customer dataset and historical churn.</p>',
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4)
    metrics = [
        ("Total customers", "8,000", "Customer base"),
        ("Historical churn", "24.89%", "Historical customer churn"),
        ("Churned customers", "1,991", "Customers classified as churned"),
        ("Analytics domains", "7", "Business analytics areas"),
    ]

    for col, (label, value, note) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                    <div class="info-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.25, 1])

    with left:
        st.markdown("### Key business signals")
        st.markdown(
            """
            - Historical churn is **24.89%** across 8,000 customers.
            - The **Basic** subscription plan has the highest recorded plan churn.
            - Payment failures, engagement, support and feedback are available
              as separate analytical domains.
            """
        )
        st.caption(
            "These are historical dataset findings, not live Netflix company metrics."
        )

    with right:
        st.markdown("### Platform capabilities")
        st.markdown(
            """
            **Data engineering**
            Structured analytics served through DuckDB.

            **Machine learning**
            Customer churn modelling across 30-, 60- and 90-day horizons.

            **AI engineering**
            Natural-language routing and grounded explanations.

            **Trust and safety**
            Deterministic analytics remain the numerical source of truth.
            """
        )

    st.info(
        "Use the Analytics explorer tab to run supported questions and inspect "
        "the underlying verified result tables."
    )


# ============================================================
# AI COPILOT
# ============================================================

with copilot_tab:
    st.markdown('<div class="section-kicker">Natural-language analytics</div>', unsafe_allow_html=True)
    st.subheader("Ask the Analytics Copilot")
    st.markdown(
        '<p class="muted">Ask a business question. The analytics engine retrieves verified results, '
        'then the explanation layer makes them easier to understand.</p>',
        unsafe_allow_html=True,
    )

    selected_question = st.session_state.pop("selected_question", "")
    if selected_question:
        st.session_state["copilot_question"] = selected_question

    question = st.text_input(
        "Business question",
        key="copilot_question",
        placeholder="e.g. Which subscription plan has the highest churn rate?",
        label_visibility="collapsed",
    )

    control_col, option_col, _ = st.columns([1.25, 1.5, 4])
    with control_col:
        run_button = st.button(
            "🔎 Ask Copilot",
            type="primary",
            use_container_width=True,
        )
    with option_col:
        use_llm = st.checkbox("AI explanation", value=True)

    if st.session_state.pop("run_selected_question", False):
        run_button = True

    if run_button:
        if not question.strip():
            st.warning("Enter a business question first.")
        else:
            with st.spinner("Querying verified business analytics..."):
                response = run_question(question, use_llm=use_llm)
            st.session_state["last_copilot_response"] = response
            st.session_state["last_copilot_question"] = question

    last_response = st.session_state.get("last_copilot_response")
    if last_response:
        st.caption(
            f"Question: {st.session_state.get('last_copilot_question', '')}"
        )
        show_copilot_result(last_response)
    else:
        st.markdown(
            """
            <div class="trust-box">
                <b>Ready when you are.</b><br>
                Start with a question about churn, subscriptions, payments,
                engagement, customer support or feedback.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ANALYTICS EXPLORER
# ============================================================

with explorer_tab:
    st.markdown('<div class="section-kicker">Explore business domains</div>', unsafe_allow_html=True)
    st.subheader("Analytics explorer")
    st.markdown(
        "Choose an analytical area to run its supported business question and "
        "inspect the returned data."
    )

    selected_domain = st.selectbox(
        "Select an analytics domain",
        list(ANALYTICS_QUESTIONS.keys()),
    )
    domain_question = ANALYTICS_QUESTIONS[selected_domain]

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">Suggested question</div>
            <div style="font-size:1.05rem;font-weight:650;color:#ffffff;">
                {domain_question}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Run domain analysis",
        type="primary",
        key="run_domain_analysis",
    ):
        with st.spinner(f"Loading {selected_domain.lower()} analytics..."):
            domain_result = run_question(domain_question, use_llm=False)
        st.session_state["domain_result"] = domain_result
        st.session_state["domain_name"] = selected_domain

    domain_result = st.session_state.get("domain_result")
    if domain_result:
        st.markdown(f"### {st.session_state.get('domain_name', 'Domain')} results")
        if domain_result.get("status") == "error":
            st.error(domain_result.get("answer", "Unable to load this domain."))
            if domain_result.get("technical_error"):
                with st.expander("Technical details"):
                    st.code(domain_result["technical_error"])
        elif domain_result.get("status") == "unsupported":
            st.warning(
                "The current analytics engine does not support this question. "
                "We can extend the routing after reviewing the engine."
            )
        else:
            display_verification(domain_result)
            display_result_table(domain_result, key_prefix="explorer")


# ============================================================
# METHODOLOGY AND LIMITATIONS
# ============================================================

with methodology_tab:
    st.markdown('<div class="section-kicker">How the platform works</div>', unsafe_allow_html=True)
    st.subheader("Methodology, grounding and limitations")

    st.markdown("### Analytics architecture")
    st.code(
        """
Business question
      ↓
Natural-language intent routing
      ↓
Approved analytics query
      ↓
DuckDB analytical layer
      ↓
Verified result table
      ↓
Optional AI explanation
        """.strip(),
        language="text",
    )

    st.markdown("### Design principles")
    st.markdown(
        """
        - **Deterministic source of truth:** numerical answers originate from
          approved analytics queries.
        - **Grounded explanations:** the AI explanation layer receives the
          verified result rather than independently calculating metrics.
        - **Safe query scope:** unsupported questions are rejected instead of
          being answered with invented business facts.
        - **Data privacy:** private source datasets and local model artefacts
          should remain outside the public repository.
        """
    )

    st.markdown("### Model evaluation")
    st.warning(
        "The recorded churn-model test AUC values were approximately 0.527 "
        "(30-day), 0.550 (60-day) and 0.568 (90-day). These indicate modest "
        "discriminative performance. Treat the models as experimental and "
        "do not present them as production-ready predictors."
    )

    st.markdown("### Scope and interpretation")
    st.caption(
        "This is a portfolio analytics project using a Netflix-themed dataset. "
        "The displayed metrics are historical dataset results and are not "
        "official or live Netflix operational statistics."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    """
    <div class="footer">
        Netflix Customer Intelligence &amp; AI Analytics Copilot<br>
        Deterministic analytics • DuckDB • Churn modelling • Grounded AI
    </div>
    """,
    unsafe_allow_html=True,
)
