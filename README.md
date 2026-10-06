# Netflix Customer Intelligence & AI Analytics Copilot

A Data Engineering and Data Science project that transforms customer, subscription, payment, viewing, support, and feedback data into verified business analytics and a grounded natural-language analytics copilot.

The project combines **Data Engineering, Data Science, Machine Learning, SQL Analytics, and AI-assisted Business Intelligence** into one end-to-end analytics system.

---

## 📌 Project Overview

Modern streaming platforms generate large amounts of customer data across multiple business functions such as:

- Customer profiles
- Subscription plans
- Payments
- Content engagement
- Customer support
- Customer feedback
- Churn behavior

The **Netflix Customer Intelligence & AI Analytics Copilot** brings these data sources together into an analytical workflow that helps answer business questions such as:

- What is the historical churn rate?
- Which subscription plans have the highest churn?
- Which customer segments have the highest churn?
- What is the payment failure rate?
- How engaged are customers with the platform?
- What are the customer-support patterns?
- What is the overall customer feedback performance?
- How can customer churn be estimated over different time horizons?

The system also provides a natural-language analytics interface so users can ask supported business questions without manually writing SQL.

---

# 🎯 What This Project Does

The project implements an end-to-end analytics pipeline covering:

- Data cleaning and quality validation
- Data transformation and feature engineering
- Customer 360 analytics
- DuckDB-based analytical storage
- Business KPI analysis
- Customer engagement analysis
- Payment analysis
- Support-ticket analysis
- Customer feedback analysis
- Churn analysis
- 30/60/90-day churn modeling
- Natural-language question routing
- Deterministic analytics execution
- Grounded AI-copilot responses
- Regression testing and safety validation

---

# 🏗️ Architecture

```text
                    Customer Data
                         │
                         ▼
              Data Engineering & Cleaning
                         │
                         ▼
                   Customer 360
                         │
                         ▼
                  DuckDB Analytics
                         │
                         ▼
             Deterministic Analytics Engine
                         │
                         ▼
           Natural-Language Intent Routing
                         │
                         ▼
             Verified Analytics Context
                         │
                         ▼
                    AI Copilot
```

The architecture intentionally separates **data computation** from **language generation**.

The analytical layer remains the source of truth, while the AI layer is used for interpretation and explanation rather than inventing business metrics.

---

# 📊 Business Analytics

The deterministic analytics engine supports business-level analysis across several areas.

## Customer Analytics

- Total customers
- Churned customers
- Non-churned customers
- Historical churn rate
- Average customer age

## Subscription Analytics

- Churn by subscription plan
- Customer distribution across plans
- Plan-level churn comparison

## Customer Segment Analytics

- Churn by customer segment
- Segment-level customer behavior
- Comparison of churn across segments

## Payment Analytics

- Total payments
- Successful payments
- Failed payments
- Payment failure rate
- Successful payment value

## Engagement Analytics

- Engagement events
- Watch hours
- Average completion rate
- Average session duration
- Active customers
- Content-level engagement

## Customer Support Analytics

- Total support tickets
- Resolved tickets
- Pending tickets
- Escalated tickets
- Average resolution time
- Customer satisfaction

## Feedback Analytics

- Total feedback records
- Average rating
- Negative feedback count
- Negative feedback rate

---

# 📈 Dataset Analytics Snapshot

The private/local project dataset contains the following analytical snapshot:

| Metric | Value |
|---|---:|
| Customers | 8,000 |
| Churned Customers | 1,991 |
| Non-Churned Customers | 6,009 |
| Historical Churn Rate | 24.89% |
| Average Customer Age | 32.58 |
| Payments | 110,735 |
| Successful Payments | 103,529 |
| Failed Payments | 7,206 |
| Payment Failure Rate | 6.51% |
| Successful Payment Value | 1,430,511.33 |
| Engagement Events | 66,422 |
| Customers with Engagement | 7,980 |
| Content Items | 500 |
| Watch Hours | 54,724.93 |
| Average Completion | 70.47% |
| Average Session Duration | 56.92 |
| Support Tickets | 6,120 |
| Customers with Support Tickets | 4,408 |
| Resolved Tickets | 3,390 |
| Pending Tickets | 888 |
| Escalated Tickets | 640 |
| Average Resolution Time | 18 hours |
| Average Support Satisfaction | 3.26 |
| Feedback Records | 5,046 |
| Customers with Feedback | 3,561 |
| Average Feedback Rating | 3.16 |
| Negative Feedback | 1,462 |
| Negative Feedback Rate | 28.97% |

> **Privacy Note:** These figures describe the private/local project dataset. Raw customer data is intentionally not included in the public GitHub repository.

---

# 🔍 Key Business Findings

## Churn by Subscription Plan

| Plan | Historical Churn |
|---|---:|
| Basic | 26.31% |
| Standard | 24.59% |
| Premium | 22.49% |

The Basic plan has the highest historical churn rate among the available subscription plans.

## Churn by Customer Segment

| Segment | Historical Churn |
|---|---:|
| Corporate | 28.06% |
| Individual | 25.03% |
| Family | 24.75% |
| Student | 22.27% |

The Corporate segment has the highest historical churn rate in the analyzed dataset.

These values are descriptive historical analytics and should not be interpreted as causal relationships.

---

# 🤖 Churn Modeling

The project includes churn models designed to estimate customer churn over multiple future horizons:

- 30-day churn
- 60-day churn
- 90-day churn

The modeling workflow includes:

1. Historical customer activity
2. Churn snapshot generation
3. Feature preparation
4. Model training
5. Probability generation
6. Validation
7. Test-set evaluation
8. Operating threshold selection

---

## Model Evaluation

The current test-set AUC results are:

| Horizon | Test AUC |
|---|---:|
| 30 Days | 0.5271 |
| 60 Days | 0.5503 |
| 90 Days | 0.5675 |

Operating thresholds were selected using validation F1:

| Horizon | Operating Threshold |
|---|---:|
| 30 Days | 0.03476 |
| 60 Days | 0.053607 |
| 90 Days | 0.080391 |

### Important Interpretation

The current AUC values are modest.

Therefore, the churn models should be treated as **experimental decision-support models**, not as highly accurate production prediction systems.

The probability generated by the model represents an estimate based on available historical features and should not be interpreted as a guarantee that a customer will churn.

---

# 🧠 AI Analytics Copilot

The project provides a natural-language interface for asking supported business analytics questions.

Example questions:

```text
What is the churn rate for Basic customers?
```

```text
Which customer segment has the highest churn?
```

```text
What is the payment failure rate?
```

The copilot processes questions through a controlled analytics workflow.

---

## Copilot Flow

```text
User Question
      │
      ▼
Intent Routing
      │
      ▼
Approved Analytics Intent
      │
      ▼
Deterministic SQL Query
      │
      ▼
DuckDB
      │
      ▼
Verified Analytics Result
      │
      ▼
Response Formatting
      │
      ▼
AI-Assisted Explanation
```

The system does **not** allow the language model to freely invent analytical queries or numerical business metrics.

---

# 🛡️ Grounding & Safety Architecture

A major design goal of this project is preventing an AI model from becoming the source of truth for business analytics.

The system therefore follows several principles.

### 1. DuckDB is the analytical source of truth

Business metrics are calculated from the analytical database rather than generated by the language model.

### 2. Approved Analytics Registry

Supported analytics are defined through an approved registry of known analytical operations.

### 3. Deterministic SQL Execution

Numerical results are produced through deterministic SQL and Python analytics logic.

### 4. Natural-Language Routing

User questions are mapped to supported analytical intents before execution.

### 5. Unsupported Questions Are Rejected Safely

If a question cannot be mapped to a supported analytics operation, the system does not fabricate an answer.

### 6. LLM Is Not the Source of Truth

Where an LLM is configured, it is used for interpretation and explanation rather than calculating or inventing business metrics.

### 7. No Unsupported Causal Claims

Historical correlations and descriptive analytics are not automatically presented as causal relationships.

### 8. Churn Probabilities Are Estimates

Model probabilities are explicitly treated as estimates rather than guarantees.

---

# 🧪 Testing

The public repository includes a regression test suite covering the core copilot behavior.

Run:

```bash
python -m unittest discover -s tests -v
```

The public regression suite contains **12 tests**.

The tests validate:

- Analytics registry
- Analytics execution contracts
- Natural-language intent routing
- Supported-question handling
- Response formatting
- Unsupported-question safety
- Deterministic analytics behavior
- No-LLM execution path
- Database interaction contracts

The public test suite is intentionally **database-independent**.

Private/local database access is mocked during testing so that the public repository can be tested without exposing customer data.

---

# 🔐 Privacy & Data Handling

This repository is intentionally packaged as a public portfolio project.

The following private assets are excluded:

- Raw customer data
- Processed/private datasets
- Local DuckDB databases
- Trained model artifacts
- Environment secrets
- API keys
- Private notebooks

The public repository contains:

- Source code
- Tests
- Documentation
- Configuration examples
- Evaluation reports

The `.env.example` file contains only a placeholder configuration and does not contain a real API key.

---

# 🧰 Technology Stack

## Programming

- Python

## Data Engineering & Analytics

- Pandas
- DuckDB
- NumPy
- PyArrow

## Machine Learning

- scikit-learn

## AI / LLM

- OpenAI-compatible API integration
- Optional local LLM experimentation

## Testing

- Python `unittest`

## Environment Management

- python-dotenv
- `.env` configuration

## Version Control

- Git
- GitHub

---

# 📁 Repository Structure

```text
netflix-customer-intelligence-ai-copilot/
│
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
│
├── src/
│   └── copilot_engine.py
│
├── tests/
│   └── test_copilot_engine.py
│
└── reports/
    ├── copilot_evaluation_report.json
    └── copilot_evaluation_results.csv
```

---

# ⚙️ Local Setup

Clone the repository:

```bash
git clone https://github.com/Basi14104/netflix-customer-intelligence-ai-copilot.git
```

Move into the project directory:

```bash
cd netflix-customer-intelligence-ai-copilot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the environment template:

```bash
copy .env.example .env
```

Configure the required environment variables only if you are using an external LLM provider.

---

# ▶️ Running the Test Suite

Run:

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 12 tests
OK
```

The public regression tests do not require:

- Private customer data
- Private DuckDB database
- OpenAI API access
- External LLM access

---

# 🗄️ Private Data Layer

The full data-backed version of the project uses a private/local DuckDB analytical database.

That database is intentionally excluded from the public repository.

### Public GitHub Repository

```text
Public Repository
│
├── Source Code
├── Tests
├── Documentation
└── Evaluation Reports
```

### Private Local Environment

```text
Private Local Environment
│
├── Raw Data
├── Processed Data
├── DuckDB Database
└── Model Artifacts
```

This separation allows the project to be demonstrated publicly without exposing customer-level data.

---

# ⚠️ Limitations

### 1. Private Dataset Is Not Published

The complete data pipeline cannot be reproduced from the public repository alone because the underlying customer dataset and local analytical database are intentionally excluded.

### 2. Churn Model Performance Is Modest

The current test AUC values are relatively low.

The models should therefore be treated as experimental decision-support tools rather than production-grade churn predictors.

### 3. External LLM Usage May Require API Access

Using a hosted LLM requires a configured provider account and available API quota.

### 4. Local CPU Inference May Be Slow

Local LLM experimentation can be impractical for interactive use on CPU-only hardware.

### 5. Public Tests Use Mocked Database Access

The public regression suite validates the application's contracts and logic without requiring private customer data.

It does not reproduce the entire private data pipeline.

---

# 📋 Project Status

## Status: Public Portfolio Release

The following components are complete:

- [x] Data engineering pipeline
- [x] Data cleaning
- [x] Customer 360 analytics
- [x] DuckDB analytical layer
- [x] Business KPI analytics
- [x] Customer engagement analytics
- [x] Payment analytics
- [x] Support analytics
- [x] Feedback analytics
- [x] Churn analysis
- [x] 30-day churn modeling
- [x] 60-day churn modeling
- [x] 90-day churn modeling
- [x] Deterministic analytics engine
- [x] Natural-language intent routing
- [x] Grounded copilot architecture
- [x] Safety controls
- [x] Regression testing
- [x] Public repository packaging
- [x] Private-data protection

---

# 🚀 Future Improvements

Potential future development areas include:

- Improved churn feature engineering
- Better model calibration
- Model explainability using feature importance or SHAP
- Additional business analytics intents
- Real-time customer analytics
- Streaming data pipelines
- Cloud data warehouse integration
- Automated data-quality monitoring
- Role-based analytics access
- Dashboard integration
- More advanced natural-language analytics
- Production-grade LLM evaluation
- Retrieval-augmented business context

---

# 💡 Engineering Principles

This project follows several principles that are important when building AI-powered analytics systems:

```text
Data First
    ↓
Deterministic Analytics
    ↓
Verified Results
    ↓
Controlled AI Interpretation
```

Rather than allowing an LLM to independently calculate business metrics, the system ensures that:

> **The database calculates the numbers.
> The analytics engine verifies the numbers.
> The AI explains the numbers.**

This separation improves reliability, traceability, and safety for business analytics.

---

# 👨‍💻 Author

**Abdul Basith U**

B.Tech — Computer Science and Business Systems
SRM Institute of Science and Technology

GitHub:
https://github.com/Basi14104

LinkedIn:
https://www.linkedin.com/in/basith-tech

---

# 📄 License

This project is currently presented as a portfolio project.

No open-source license has been added to the repository at this time.
