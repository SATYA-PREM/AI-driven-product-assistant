# AI-Driven Product Assistant & Product Intelligence Platform

An enterprise-grade autonomous AI multi-agent platform designed to ingest raw customer feedback, reviews, and support tickets, enforce rigorous Pydantic-based data validation, clean and normalize records, isolate and quarantine dirty data, extract deep AI-ready ProductSignals, and power strategic product intelligence via CrewAI multi-agent orchestration.

---

## 🌟 Key Capabilities

1. **Multi-Format Ingestion**: Ingests Customer Feedback, Product Reviews, and Support Tickets across CSV, JSON, and Excel (`.xlsx`).
2. **Pydantic v2 Schema & Business Rule Validation**: Strict schema enforcement, numeric rating constraints, text length checks, and duplicate detection.
3. **Dual Storage Strategy (Cleaned vs. Dirty Quarantine)**:
   - Valid normalized records are stored in MongoDB `cleaned_data`.
   - Defective and rejected records are isolated in `dirty_data` with defect tags (`corrupted`, `missing_fields`, `schema_defect`).
4. **AI-Ready ProductSignals**: Valid data is deeply preprocessed with intent tagging (`bug_report`, `feature_request`, `praise`, `churn_risk`), token metrics, and keywords, stored in `ai_preprocessed_data`.
5. **Product Manager (PM) Salvage Promotion**: Audits dirty data for recoverable customer complaints missing non-critical metadata, stages them in `salvaged_data`, and elevates PM-approved records directly into the production AI signal stream.
6. **CrewAI Multi-Agent System**:
   - **`PreprocessingAgent`**: Dedicated CrewAI agent orchestrating the end-to-end data lifecycle.
   - **`ProductIntelligenceCrew`**: Multi-agent coordinator ready to orchestrate future downstream agents (`InsightsAgent`, `StrategyAgent`).
7. **Interactive Swagger UI**: 44 fully documented REST endpoints across 19 operational categories at `/docs`.

---

## 🏗️ Project Architecture

```
backend/
├── app/
│   ├── agents/
│   │   ├── preprocessing_agent/        # Primary Preprocessing Agent (CrewAI)
│   │   │   ├── agent.py               # Agent, Tasks, Crew factory & service wrapper
│   │   │   ├── prompts.py             # Agent role, goal, backstory & task prompts
│   │   │   └── tools.py               # CrewAI @tool wrappers & backend delegators
│   │   ├── crew.py                    # Multi-Agent Coordinator (ProductIntelligenceCrew)
│   │   ├── llm.py                     # Centralized Gemini LLM configuration
│   │   └── __init__.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py                # JWT authentication & signup
│   │   │   ├── users.py               # User profiles
│   │   │   ├── workspaces.py          # Workspace lifecycle & members
│   │   │   ├── products.py            # Product catalogs
│   │   │   ├── data.py                # File upload & raw records
│   │   │   ├── validation.py          # Pydantic validation & reports
│   │   │   ├── cleaning.py            # Cleaning, normalization & dirty data
│   │   │   ├── preprocessing.py       # AI signals & usability reports
│   │   │   ├── pm_validation.py       # PM review & salvage promotion
│   │   │   ├── analysis.py            # AI deep analysis
│   │   │   ├── intelligence.py        # Sentiment & trends
│   │   │   ├── assistant.py           # AI Product Assistant natural language query
│   │   │   ├── phases.py              # Pipeline phase tracking
│   │   │   ├── reports.py             # Executive intelligence reporting
│   │   │   ├── tasks.py               # Backlog tasks & action items
│   │   │   ├── jobs.py                # Processing job monitoring
│   │   │   ├── workflow.py            # Multi-step workflow state
│   │   │   └── health.py              # System & MongoDB health checks
│   │   └── router.py                  # Master v1 router aggregating all endpoints
│   ├── core/                          # Config, database, security, and logging
│   ├── middleware/                    # Auth, logging, and error handling
│   ├── models/                        # MongoDB document data models
│   ├── repositories/                  # MongoDB collection queries & persistence
│   ├── schemas/                       # Pydantic v2 request & response schemas
│   ├── services/                      # Business logic layer (Ingestion, Validation, Cleaning, NLP)
│   ├── utils/                         # Date, text, and serialization utilities
│   └── main.py                        # FastAPI entry point with CORS & Lifespan
├── tests/
│   ├── api/                           # Endpoint API integration tests
│   ├── integration/                   # Pipeline & workflow integration tests
│   └── unit/                          # Unit tests (Agents, Pydantic, Parsers)
├── requirements.txt
└── start_server.bat
```

---

## 🗄️ MongoDB Storage Architecture

Data flows through dedicated collections to guarantee zero data loss and separation of concerns:

| Collection | Purpose |
| :--- | :--- |
| `raw_data` | Untouched, pristine records exactly as ingested from CSV/JSON/Excel. |
| `validation_results` | Quality score, error counts, and per-record validation logs. |
| `cleaned_data` | Valid records after normalization (dates, text casing, duplicate elimination). |
| `dirty_data` | Invalid records quarantined with defect types (`corrupted`, `missing_fields`). |
| `ai_preprocessed_data` | Canonical AI-ready `ProductSignal` records with intent tags and keyword tokens. |
| `salvaged_data` | Recoverable feedback from dirty data undergoing Product Manager (PM) review. |
| `ai_analyses` | Deep synthesis of sentiment distribution, themes, and feature recommendations. |
| `assistant_requests` | Natural language chat questions and cited feedback signals. |
| `reports` | Executive intelligence reports and actionable summaries. |
| `tasks` | Engineering/design backlog tasks generated from feedback analysis. |

---

## 👥 User Roles & Role-Based Access Control (RBAC)

The platform enforces fine-grained Role-Based Access Control across **5 specialized roles**, allowing cross-functional collaboration between Product, Engineering, Design, Data, and Customer teams:

| Role Name | Identifier (`role`) | Core Responsibilities & Focus |
| :--- | :--- | :--- |
| **Product Manager** | `product_manager` | Workspace ownership, PRD generation, roadmaps, executive intelligence, and dirty data salvage review & promotion into active AI signals. |
| **Data Engineer** | `data_engineer` | Dataset ingestion (CSV/JSON/Excel), pipeline triggers (validation, cleaning, AI preprocessing), dataset deletion, and data quality audits. |
| **Product Designer** | `product_designer` | UX friction analysis, user sentiment trends, feedback review, and UX/design backlog task execution. |
| **Engineering Lead** | `engineering_lead` | Defect tracking, bug analysis from customer feedback, technical feasibility audits, and engineering task assignment. |
| **Customer Success** | `customer_success` | Support ticket analysis, churn risk escalation, customer sentiment monitoring, and support dataset ingestion. |

### 🔑 Permissions Matrix

| Permission | `product_manager` | `data_engineer` | `product_designer` | `engineering_lead` | `customer_success` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Create / Manage Workspaces** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Create / Edit Products** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Upload Datasets** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Run Pipeline (Clean/Preprocess)** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Delete Datasets** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **PM Salvage Review & Promotion** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Generate PRDs & Strategy Plans** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Assign Backlog Tasks** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **View Intelligence & Insights** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **View & Complete Tasks** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🚀 Quick Start Guide


### 1. Prerequisites
- Python 3.11+
- Node.js 18+ (for Frontend)
- MongoDB (Local instance or MongoDB Atlas URI)
- Google Gemini API Key (Optional, for autonomous LLM agent execution)

### 2. Backend Setup
```bash
cd backend

# Create & activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Open .env and configure your MONGODB_URL and optional GEMINI_API_KEY
```

### 3. Start Backend Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```
* **API Root**: [http://localhost:8000](http://localhost:8000)
* **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
* **Frontend UI**: [http://localhost:5173](http://localhost:5173)

---

## 📑 Complete Swagger API Reference (`/docs`)

All 44 operations across 19 tags are accessible interactively in Swagger UI:

### 1. Data Ingestion & Raw Storage (`/api/v1/data`)
* `POST /api/v1/data/upload`: Upload and ingest CSV, JSON, or Excel dataset.
* `GET /api/v1/data/datasets`: List all uploaded datasets in a workspace.
* `GET /api/v1/data/datasets/{dataset_id}`: Retrieve dataset metadata.
* `GET /api/v1/data/datasets/{dataset_id}/raw`: Query raw stored records.
* `GET /api/v1/data/datasets/{dataset_id}/export`: Export dataset.

**Canonical Enterprise CSV Format**:
```csv
feedback_id,feedback_date,customer_segment,platform,module,feedback_text,browser_or_client,device_or_os,country,source,customer_type,rating,created_at
FB001,2026-02-01,Enterprise,Web App,Checkout,"I clicked pay twice because the first click looked like nothing happened...",Chrome 131,Windows 11,USA,Email,Returning,2,2026-02-01T09:12:00Z
```
*Validated via Pydantic v2 with granular business rules, date parsing, numeric rating constraints (1–5), and preservation of all product dimensions (`module`, `platform`, `customer_segment`, `country`, `device_or_os`, `source`, `customer_type`).*

### 2. Pydantic Validation (`/api/v1/validation`)
* `POST /api/v1/validation/validate`: Run Pydantic v2 schema & business rule validation.
* `GET /api/v1/validation/{dataset_id}`: Retrieve validation quality score & errors.

### 3. Cleaning & Normalization (`/api/v1/cleaning`)
* `POST /api/v1/cleaning/clean`: Run normalization, deduplication, and quarantine dirty records.
* `GET /api/v1/cleaning/{dataset_id}`: Retrieve cleaned records and dirty quarantine count.

### 4. AI Preprocessing (`/api/v1/preprocessing`)
* `POST /api/v1/preprocessing/preprocess`: Preprocess valid records into `ai_preprocessed_data`.
* `GET /api/v1/preprocessing/{dataset_id}`: Retrieve AI signal counts and status.
* `GET /api/v1/preprocessing/{dataset_id}/usability-report`: Comprehensive dataset health & usability score.

### 5. PM Validation & Dirty Data Salvage (`/api/v1/pm-validation`)
* `GET /api/v1/pm-validation/candidates/{dataset_id}`: List dirty records staged for PM review.
* `POST /api/v1/pm-validation/audit/{dataset_id}`: Trigger dirty data audit to discover salvageable feedback.
* `POST /api/v1/pm-validation/review`: Approve or reject a candidate salvaged record.
* `POST /api/v1/pm-validation/promote`: Promote PM-approved salvaged records into the production AI signal stream.

### 6. AI Analysis & Insights (`/api/v1/analysis`, `/api/v1/intelligence`)
* `POST /api/v1/analysis/trigger`: Run automated sentiment, theme, and recommendation analysis.
* `GET /api/v1/analysis/dataset/{dataset_id}`: Retrieve latest AI analysis.
* `GET /api/v1/intelligence/summary/{workspace_id}`: Health score, NPS estimate, and complaints.
* `GET /api/v1/intelligence/sentiment/{workspace_id}`: Granular sentiment breakdown.

### 7. AI Product Assistant (`/api/v1/assistant`)
* `POST /api/v1/assistant/ask`: Ask natural language questions with feedback citations.
* `GET /api/v1/assistant/history/{workspace_id}`: Query history log.

### 8. Executive Reports & Tasks (`/api/v1/reports`, `/api/v1/tasks`)
* `POST /api/v1/reports/generate`: Generate executive intelligence reports.
* `GET /api/v1/reports/{workspace_id}`: List reports.
* `POST /api/v1/tasks`: Create product engineering tasks from feedback findings.
* `GET /api/v1/tasks/{workspace_id}`: View action items.
* `PATCH /api/v1/tasks/{task_id}`: Update task status (todo, in_progress, done).

### 9. Core Operations (`/api/v1/auth`, `workspaces`, `products`, `jobs`, `workflow`, `health`)
* **User Registration with Role Preference**: `POST /api/v1/auth/register`
  Enables selecting a primary professional role upon registration. Supported roles: `product_manager`, `data_engineer`, `product_designer`, `engineering_lead`, `customer_success`.
  ```json
  {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "password": "StrongPassword123!",
    "role": "data_engineer"
  }
  ```
  *(If omitted, default role is `product_manager`)*
* **User Login**: `POST /api/v1/auth/login` (Returns JWT Bearer token and user profile)
* **Workspaces & Catalogs**: Multi-tenant workspace isolation (`/workspaces`), team member invitations, and product catalog management (`/products`).
* **Jobs & Workflow**: Processing job monitors (`/jobs`), pipeline phases (`/phases`), and step-by-step pipeline state machines (`/workflow`).
* **Health**: Comprehensive system & MongoDB connection checks (`/health`).

---

## 🤖 CrewAI Preprocessing Agent Usage

You can invoke the Preprocessing Agent programmatically or let CrewAI orchestrate tasks autonomously:

```python
from app.agents import preprocessing_agent, crew_manager

# 1. Direct programmatic execution
results = preprocessing_agent.run_full_pipeline(
    dataset_id="ds_customer_feedback_01",
    workspace_id="ws_production",
)
print("Usability Rate:", results["usability_report"]["usability_rate_percent"])

# 2. Autonomous CrewAI Kickoff
crew = crew_manager.build_preprocessing_crew(
    dataset_id="ds_customer_feedback_01",
    workspace_id="ws_production",
)
crew_output = crew.kickoff()
print("CrewAI Output:", crew_output)
```

---

## 🧪 Running Tests

Execute the full backend test suite:
```bash
pytest tests/ -v
```
All unit tests, Pydantic validation tests, and pipeline integration tests run with standard mocks and fixtures.
