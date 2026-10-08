import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "src"

if str(SOURCE_PATH) not in sys.path:
    sys.path.insert(0, str(SOURCE_PATH))


# ============================================================
# COPILOT IMPORT
# ============================================================

from copilot_engine import ask


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Customer Intelligence Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #141414 0%,
            #242424 100%
        );
        border: 1px solid #333333;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #b8b8b8;
    }

    .metric-card {
        padding: 1.2rem;
        border-radius: 14px;
        background: #181818;
        border: 1px solid #303030;
        text-align: center;
    }

    .metric-label {
        color: #a0a0a0;
        font-size: 0.85rem;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .answer-box {
        padding: 1.4rem;
        border-radius: 14px;
        background: #181818;
        border: 1px solid #303030;
        margin-top: 1rem;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 650;
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    .status-success {
        color: #7ee787;
        font-weight: 600;
    }

    .status-warning {
        color: #f2cc60;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📊 Copilot")

    st.markdown(
        """
        **Netflix Customer Intelligence**

        A grounded analytics copilot that combines:

        - Customer analytics
        - Churn analytics
        - Subscription analytics
        - Payment analytics
        - Engagement analytics
        - Support analytics
        - Feedback analytics
        - Local LLM explanations
        """
    )

    st.divider()

    st.markdown("### 🔐 Grounding")

    st.success(
        "Verified analytics are generated from the deterministic "
        "DuckDB analytics layer."
    )

    st.caption(
        "The LLM explains verified results. "
        "It is not the source of numerical truth."
    )

    st.divider()

    st.markdown("### 💡 Example questions")

    examples = [
        "What is our overall churn rate?",
        "Which subscription plan has the highest churn rate?",
        "Which customer segment has the highest churn?",
        "What is the payment failure rate?",
        "How much are customers watching?",
        "How many support tickets do we have?",
        "What is the average customer rating?",
    ]

    for example in examples:
        if st.button(
            example,
            key=f"example_{example}",
            use_container_width=True,
        ):
            st.session_state["question"] = example


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            📊 Netflix Customer Intelligence & AI Analytics Copilot
        </div>
        <div class="hero-subtitle">
            Ask business questions and receive verified analytics
            with grounded AI explanations.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI HEADER
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Customers</div>
            <div class="metric-value">8,000</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Historical Churn</div>
            <div class="metric-value">24.89%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Churned Customers</div>
            <div class="metric-value">1,991</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Analytics Domains</div>
            <div class="metric-value">7</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# QUESTION INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Ask the Analytics Copilot</div>',
    unsafe_allow_html=True,
)

question = st.text_input(
    "Business question",
    value=st.session_state.get("question", ""),
    placeholder="e.g. Which subscription plan has the highest churn rate?",
    label_visibility="collapsed",
)


# ============================================================
# CONTROLS
# ============================================================

col_button, col_llm, col_space = st.columns([1.2, 1.2, 3])

with col_button:
    ask_button = st.button(
        "🔎 Ask Copilot",
        type="primary",
        use_container_width=True,
    )

with col_llm:
    use_llm = st.checkbox(
        "🤖 AI explanation",
        value=True,
    )


# ============================================================
# PROCESS QUESTION
# ============================================================

if ask_button and question.strip():

    with st.spinner("Analyzing verified business data..."):

        response = ask(
            question.strip(),
            use_llm=use_llm,
        )

    # --------------------------------------------------------
    # UNSUPPORTED QUESTION
    # --------------------------------------------------------

    if response.get("status") == "unsupported":

        st.warning(
            "This question is outside the currently supported "
            "Netflix business analytics scope."
        )

    # --------------------------------------------------------
    # SUCCESSFUL RESPONSE
    # --------------------------------------------------------

    else:

        st.markdown(
            '<div class="section-title">Copilot Answer</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="answer-box">
                {response.get("answer", "No answer generated.")}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # RESPONSE METADATA
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Verification Details</div>',
            unsafe_allow_html=True,
        )

        meta1, meta2, meta3 = st.columns(3)

        with meta1:
            st.caption("Intent")
            st.code(
                str(response.get("intent", "N/A")),
                language=None,
            )

        with meta2:
            st.caption("Analytics Query")
            st.code(
                str(response.get("query_name", "N/A")),
                language=None,
            )

        with meta3:
            st.caption("Source")
            st.code(
                str(response.get("source", "N/A")),
                language=None,
            )

        # ----------------------------------------------------
        # RAW VERIFIED DATA
        # ----------------------------------------------------

        data = response.get("data")

        if data is not None:

            st.markdown(
                '<div class="section-title">Verified Analytics</div>',
                unsafe_allow_html=True,
            )

            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True,
            )

        # ----------------------------------------------------
        # CALCULATION MODE
        # ----------------------------------------------------

        calculation_mode = response.get(
            "calculation_mode",
            "deterministic_sql",
        )

        st.caption(
            f"Calculation mode: `{calculation_mode}`"
        )


# ============================================================
# EMPTY STATE
# ============================================================

elif not question.strip():

    st.info(
        "Enter a business question above or choose an example "
        "from the sidebar."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Netflix Customer Intelligence & AI Analytics Copilot • "
    "Deterministic analytics + grounded local AI"
)