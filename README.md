<div align="center">

# IntelCredit

### AI-Powered Corporate Credit Appraisal Engine

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Next-Gen Corporate Credit Appraisal: Bridging the Intelligence Gap*

An AI-powered Credit Decisioning Engine that automates the end-to-end preparation of a **Comprehensive Credit Appraisal Memo (CAM)** with explainable scoring, multi-source data integration, and India-context intelligence.

[**Getting Started**](#-getting-started) · [**Features**](#-features) · [**Architecture**](#-architecture) · [**API Docs**](#-api-endpoints) · [**Demo**](#-quick-demo)

</div>

---

## Highlights

- **End-to-End Pipeline** — From document upload to a print-ready 12-section Credit Appraisal Memo
- **Explainable Five Cs Scoring** — Deterministic, auditable, rule-based engine with full transparency
- **India-Context Intelligence** — GST (GSTR-1/3B/2A), CIBIL, MCA, NCLT, CIN/PAN/GSTIN validation
- **Multi-Format Parsing** — PDF, Excel, CSV, JSON across 8 document types
- **Triple Cross-Check** — Revenue verification across GST, bank credits, and reported financials
- **One-Click Demo** — Full pipeline demo with sample data — no documents needed

---

## Table of Contents

- [Highlights](#highlights)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Quick Demo](#-quick-demo)
- [Page-by-Page Guide](#-page-by-page-guide)
- [Data Flow](#-end-to-end-data-flow)
- [Five Cs Scoring Model](#-five-cs-scoring-model)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Indian Context](#-indian-context)
- [ML Approach](#-does-this-project-use-ml)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔄 How It Works

IntelCredit is an **end-to-end credit appraisal platform** designed for Indian corporate lending. It takes a company's financial documents (annual reports, GST returns, bank statements, ITR, legal notices, etc.), runs automated analysis, scores the borrower on 5 dimensions, and generates a professional **Credit Appraisal Memo (CAM)** — the document banks use to approve or reject loans.

### The Pipeline

```
 ┌───────────────┐    ┌──────────────────┐    ┌──────────────────────┐
 │ 1. Company    │───▶│ 2. Document      │───▶│ 3. Financial         │
 │    Profile    │    │    Upload/Parse   │    │    Analysis          │
 │ (basic info)  │    │ (PDF,Excel,CSV)   │    │ (ratios,GST,banking) │
 └───────────────┘    └──────────────────┘    └──────────┬───────────┘
                                                         │
 ┌───────────────┐    ┌──────────────────┐    ┌──────────▼───────────┐
 │ 6. CAM Report │◀───│ 5. Credit        │◀───│ 4. Research +        │
 │    (HTML doc) │    │    Scoring (5Cs)  │    │    Primary Insights  │
 └───────────────┘    └──────────────────┘    └──────────────────────┘
```

| Step | Description |
|------|-------------|
| **1. Company Profile** | Enter company details — CIN, PAN, GSTIN, promoters, industry, loan request |
| **2. Data Ingestor** | Upload financial documents. Uses **PyMuPDF** for PDFs and **Pandas** for spreadsheets with regex extractors for Indian formats (₹ Crore/Lakhs, GSTIN, CIN). Supports 8 document types |
| **3. Financial Analysis** | Computes 14+ ratios (EBITDA margin, D/E, ICR, DSCR, current ratio, ROE, etc.), GST cross-verification, bank statement analysis, and **triple cross-check** of revenue |
| **4. Research + Insights** | Automated secondary research — news sentiment, litigation (NCLT/e-Courts), regulatory compliance, sector analysis, management background. Plus qualitative primary insights |
| **5. Credit Scoring** | **Five Cs** framework scoring — deterministic, explainable, with weighted score (0–100), risk category, and loan decision |
| **6. CAM Report** | **12-section professional HTML** CAM with executive summary, financial tables, score bars, risk assessment, recommendation. Print-ready |

---

## ✨ Features

### Three Pillars

| Pillar | Description |
|--------|------------|
| **📄 Data Ingestor** | Multi-format document parsing (PDF, Excel, CSV, JSON) for GST returns, bank statements, ITR, annual reports, legal notices, rating reports, sanction letters |
| **🔍 Research Agent** | Automated secondary research across 6 modules: news sentiment, litigation (NCLT/e-Courts), regulatory compliance (MCA/GST), sector risk analysis, management background, MCA filings |
| **📊 Recommendation Engine** | Explainable Five Cs credit scoring with auto-generated 12-section CAM report, loan decision, interest rate pricing, and risk-based conditions |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   React Frontend (Vite)                  │
│                                                          │
│   Dashboard │ Company Profile │ Data Ingestor            │
│   Financial Analysis │ Research Agent │ Primary Insights │
│   Credit Scoring │ CAM Report                            │
└──────────────────────────┬───────────────────────────────┘
                           │ REST API (JSON)
┌──────────────────────────┴───────────────────────────────┐
│                  FastAPI Backend (Python)                 │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────┐  ┌───────────────────────────────┐  │
│  │ Document Parser  │  │  Financial Analyzer           │  │
│  │ (PyMuPDF,Pandas) │  │  (Ratios, GST, Bank, Trends) │  │
│  └─────────────────┘  └───────────────────────────────┘  │
│                                                          │
│  ┌─────────────────┐  ┌───────────────────────────────┐  │
│  │ Research Agent   │  │  Scoring Engine (Five Cs)     │  │
│  │ (6 modules)     │  │  (Rule-based, Explainable)    │  │
│  └─────────────────┘  └───────────────────────────────┘  │
│                                                          │
│  ┌─────────────────┐  ┌───────────────────────────────┐  │
│  │ CAM Generator   │  │  In-Memory Database           │  │
│  │ (HTML report)   │  │  (Prototype storage)          │  │
│  └─────────────────┘  └───────────────────────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19 + Vite 6 + React Router 6 + Recharts + Lucide Icons |
| **Backend** | Python FastAPI + Pydantic v2 + Uvicorn |
| **Scoring** | Custom explainable rule-based engine (Five Cs framework) |
| **Document Parsing** | PyMuPDF (fitz), Pandas, openpyxl, python-docx, tabula-py |
| **Report Generation** | HTML with inline CSS (self-contained, print-ready) |
| **Database** | In-memory Python dicts (hackathon prototype) |
| **Research** | Simulated modules (architecture ready for real APIs) |
| **India-Specific** | GST (GSTR-1/3B/2A), CIBIL, CIN, MCA, NCLT, DRT, e-Courts |

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.9+
- **Node.js** 18+

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/intelcredit.git
cd intelcredit
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

> Backend runs on **http://localhost:8000** — API docs available at **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

> Dev server runs on **http://localhost:3000** with API proxy to backend port 8000

### 4. Production Build

```bash
cd frontend
npm run build
# Built files go to frontend/dist/
# Backend auto-serves them at http://localhost:8000
```

---

## 🎮 Quick Demo

> **No documents needed** — try the full pipeline with sample data in one click.

1. Start both backend and frontend
2. Open **http://localhost:3000** (dev) or **http://localhost:8000** (prod)
3. Go to **CAM Report** page → Click **"Generate Demo CAM"**
4. The system runs the entire pipeline with sample data for "Bharat Manufacturing Pvt Ltd":

   | Pipeline Step | What Happens |
   |---------------|-------------|
   | Financial Data | 3 years of data → ratio computation |
   | GST Analysis | 12 months → mismatch detection |
   | Bank Analysis | 12 months → cheque bounce analysis |
   | Research | News, litigation, regulatory, sector |
   | Scoring | Five Cs → weighted score + decision |
   | CAM Report | 12-section HTML document |

---

## 📖 Page-by-Page Guide

<details>
<summary><b>1. Dashboard</b> — <code>/</code></summary>

Landing page with welcome banner, Five Cs wheel visualization (SVG), quick-start buttons ("Generate Demo CAM" / "Start New Appraisal"), stats overview (12+ doc types, 25+ ratios, 6 research sources), and a 6-step pipeline diagram.

</details>

<details>
<summary><b>2. Company Profile</b> — <code>/company</code></summary>

Editable form pre-filled with demo company data. Enter company identifiers (CIN, PAN, GSTIN), promoter details, industry type, existing credit rating, and loan request details (amount, purpose, tenure, collateral). Saves to in-memory database and localStorage.

</details>

<details>
<summary><b>3. Data Ingestor</b> — <code>/documents</code></summary>

**Drag-and-drop upload zone** supporting 8 document types (Annual Report, Financial Statements, GST Returns, Bank Statements, ITR, Legal Notices, Sanction Letters, Rating Reports). Upload real documents or use **"Simulate Extraction"** buttons to generate realistic parsed data for demo. Parser uses regex patterns tailored for Indian financial formats.

</details>

<details>
<summary><b>4. Financial Analysis</b> — <code>/financials</code></summary>

**Tabbed interface** with 5 tabs:
- **Input Data** – Enter multi-year financials (revenue, EBITDA, PAT, assets, liabilities) or load sample 3-year data
- **Ratios** – Computed financial ratios with benchmarks and pass/fail indicators
- **GST** – GST return analysis with mismatch flags
- **Banking** – Bank statement analysis (cheque bounces, EMI regularity, trends)
- **Flags** – Anomalies and red flags from cross-verification

</details>

<details>
<summary><b>5. Research Agent</b> — <code>/research</code></summary>

One-click **"Run Secondary Research"** button that runs 6 research modules in parallel: news analysis (with sentiment scoring), litigation check (NCLT/e-Courts), regulatory compliance (ROC/GST/IT), sector analysis (with industry-specific risks), management background check, and MCA filing status. Results displayed as color-coded cards.

</details>

<details>
<summary><b>6. Primary Insights</b> — <code>/insights</code></summary>

Add qualitative observations from site visits, management interviews, or field research. Each insight has a category, impact level (positive/neutral/negative), and description. Keyword matching adjusts the credit score (negative keywords → score penalty; positive keywords → score boost). Capped at -30 to +20 adjustment.

</details>

<details>
<summary><b>7. Credit Scoring</b> — <code>/scoring</code></summary>

Displays the **Five Cs scoring results** with:
- Circular SVG gauge showing weighted score (0–100)
- Risk badge (LOW / MODERATE / HIGH / VERY HIGH)
- Decision badge (APPROVED / CONDITIONAL / REJECTED)
- Horizontal bar charts for each C with individual scores and weights
- Recommended loan amount, interest rate, and tenure
- Step-by-step explanation of the scoring logic and any conditions

</details>

<details>
<summary><b>8. CAM Report</b> — <code>/cam</code></summary>

The final output. Two modes:
- **"Generate Demo CAM"** – Uses sample data for the full pipeline
- **"Generate from Data"** – Uses data you entered in previous steps

Produces a **12-section HTML Credit Appraisal Memo** rendered in an iframe:

| # | Section |
|---|---------|
| 1 | Header & Confidentiality Notice |
| 2 | Executive Summary (AI-generated narrative) |
| 3 | Company Overview |
| 4 | Loan Proposal (requested vs recommended) |
| 5 | Financial Analysis (ratio grid, GST table, bank table) |
| 6 | Five Cs Assessment (score bars per pillar) |
| 7 | Secondary Research Findings |
| 8 | Primary Due Diligence |
| 9 | Risk Assessment (severity levels + mitigants) |
| 10 | Recommendation & Verdict |
| 11 | Terms & Conditions |
| 12 | Annexures (methodology, disclaimer) |

Includes **Print** and **Download JSON** buttons.

</details>

---

## 🔀 End-to-End Data Flow

```
User enters company details
        │
        ▼
Upload documents (PDF/Excel/CSV/JSON)
   └─── document_parser.py ──── regex extraction ──── structured JSON
        │
        ▼
Financial Analysis
   ├── compute_financial_ratios()  → 14+ ratios with benchmarks
   ├── analyze_gst_data()         → GSTR-1/3B mismatch, circular trading
   ├── analyze_bank_statements()  → cheque bounces, EMI, trends
   ├── cross_verify_revenue()     → GST vs Bank vs Reported (3-way check)
   └── compute_trend_analysis()   → CAGR, trajectory, loss detection
        │
        ▼
Research + Insights
   ├── research_agent → news, litigation, regulatory, sector, management, MCA
   └── primary insights → keyword-based score adjustment (-30 to +20)
        │
        ▼
Credit Scoring (Five Cs Engine)
   ├── Character (20%)  → wilful defaulter, litigation, compliance, sentiment
   ├── Capacity  (25%)  → EBITDA margin, ICR, DSCR, revenue growth
   ├── Capital   (20%)  → D/E ratio, net worth, current ratio, ROE
   ├── Collateral(15%)  → coverage ratio, collateral type, charges
   └── Conditions(20%)  → sector outlook, regulatory, peer comparison
        │
        ▼
Weighted Score (0-100) → Risk Category → Loan Decision
   ├── Low Risk (75-100)   → Approve 100%, +1.5% rate, 60 months
   ├── Moderate (50-74)    → Approve 75%, +3.0% rate, 48 months
   ├── High (25-49)        → Conditional 50%, +5.0% rate, 36 months
   └── Very High (0-24)    → Reject
        │
        ▼
CAM Report (12-section HTML document, print-ready)
```

---

## 📊 Five Cs Scoring Model

| Pillar | Weight | Base Score | Key Scoring Factors |
|--------|--------|------------|---------------------|
| **Character** | 20% | 75 | Wilful defaulter (-50), director disqualification (-30), litigation count (±10–20), ROC/GST compliance (±5–10), news sentiment (±5–15), management experience (+2–5) |
| **Capacity** | 25% | 50 | EBITDA margin vs benchmarks (±15), interest coverage (±15), DSCR (±15), revenue growth trajectory (±10–20), cheque bounces (±5–15), GST anomaly flags (-3 each) |
| **Capital** | 20% | 50 | D/E ratio (±20), net worth tiers (±10–25), current ratio (±15), ROE contribution |
| **Collateral** | 15% | 50 | Coverage ratio (±5–25), collateral type (+3–10), existing charge count (-5–10) |
| **Conditions** | 20% | 60 | Sector outlook scoring, regulatory environment, peer comparison, sector-specific risks, growth forecast |

<details>
<summary><b>Auto-Reject Triggers</b></summary>

- Character score < 25 (integrity failure)
- Capacity score < 20 (unable to service debt)
- Weighted score < 25 (overall risk too high)

</details>

<details>
<summary><b>Interest Rate Pricing</b></summary>

| Risk Level | Spread | Total Rate |
|------------|--------|------------|
| Base rate (RBI repo + spread) | — | 8.50% |
| Low risk | +1.50% | 10.00% |
| Moderate risk | +3.00% | 11.50% |
| High risk | +5.00% | 13.50% |
| Very high risk | Rejected | — |

**Loan Amount Cap:** Minimum of 2.5× Net Worth, 4× EBITDA, requested amount × risk multiplier

</details>

---

## 🌐 API Endpoints

<details>
<summary><b>Documents</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents/upload` | Upload & parse a financial document (PDF/Excel/CSV/JSON) |
| `POST` | `/api/documents/parse-sample/{type}` | Generate simulated extraction for demo |
| `GET` | `/api/documents/list` | List all parsed documents |
| `GET` | `/api/documents/{doc_id}` | Get specific document data |

</details>

<details>
<summary><b>Financial Analysis</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analysis/ratios` | Compute ratios for a single year |
| `POST` | `/api/analysis/gst` | Analyze GST returns |
| `POST` | `/api/analysis/banking` | Analyze bank statements |
| `POST` | `/api/analysis/cross-verify` | Cross-verify revenue across sources |
| `POST` | `/api/analysis/full` | **Full financial analysis pipeline** |

</details>

<details>
<summary><b>Research</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/research/secondary` | Run all 6 secondary research modules |
| `POST` | `/api/research/insights` | Add a primary due diligence insight |
| `GET` | `/api/research/insights/{id}` | Get insights for a company |
| `POST` | `/api/research/insights/adjust-score` | Adjust score based on insights |

</details>

<details>
<summary><b>CAM Report</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/cam/generate` | **Master endpoint** — runs full pipeline, generates CAM |
| `POST` | `/api/cam/generate-html` | Generate CAM as HTML only |
| `POST` | `/api/cam/demo` | **Demo** — full pipeline with sample data |
| `GET` | `/api/cam/report/{id}` | Retrieve a stored CAM report |
| `GET` | `/api/cam/reports` | List all CAM reports |

</details>

> **Full Swagger docs** available at `/docs` and ReDoc at `/redoc` when backend is running.

---

## 📁 Project Structure

```
intelcredit/
├── backend/
│   ├── main.py                   # FastAPI entry point, CORS, router mounting
│   ├── config.py                 # App config, Five Cs weights, risk thresholds
│   ├── requirements.txt          # Python dependencies
│   ├── ml_models/                # Reserved for future ML model files (.pkl/.joblib)
│   ├── uploads/                  # Uploaded document storage
│   ├── models/
│   │   ├── schemas.py            # Pydantic models (Company, Loan, Financial, etc.)
│   │   └── database.py           # In-memory storage (Python dicts with UUID keys)
│   ├── services/
│   │   ├── document_parser.py    # Multi-format parser, 8 document type extractors
│   │   ├── financial_analyzer.py # Ratio engine, GST cross-check, bank analysis
│   │   ├── research_agent.py     # 6-module research (news, litigation, regulatory...)
│   │   ├── scoring_engine.py     # Five Cs rule-based scoring, decision logic
│   │   └── cam_generator.py      # 12-section HTML CAM report builder
│   └── routers/
│       ├── documents.py          # Document upload/parse/list APIs
│       ├── analysis.py           # Financial analysis APIs
│       ├── research.py           # Research & insights APIs
│       └── cam.py                # CAM generation orchestration APIs
├── frontend/
│   ├── package.json              # React 19, Vite, React Router, Recharts, Lucide
│   ├── vite.config.js            # Dev server proxy to backend :8000
│   ├── index.html                # SPA entry point
│   └── src/
│       ├── main.jsx              # React DOM render
│       ├── App.jsx               # React Router setup (8 routes)
│       ├── context/
│       │   └── AppContext.jsx     # Global state (useReducer + Context)
│       ├── services/
│       │   └── api.js            # Fetch-based API client
│       ├── components/
│       │   ├── Layout.jsx        # App shell with sidebar + topbar
│       │   ├── Sidebar.jsx       # Navigation with Lucide icons
│       │   ├── Toast.jsx         # Notification toasts
│       │   └── LoadingOverlay.jsx # Full-screen loading spinner
│       ├── pages/
│       │   ├── Dashboard.jsx     # Landing page, Five Cs wheel
│       │   ├── CompanyProfile.jsx# Company/loan details form
│       │   ├── DataIngestor.jsx  # Document upload + simulated extraction
│       │   ├── FinancialAnalysis.jsx # Multi-year financials + ratio analysis
│       │   ├── ResearchAgent.jsx # Secondary research runner + results
│       │   ├── PrimaryInsights.jsx # Qualitative observation entry
│       │   ├── CreditScoring.jsx # Five Cs score gauge + decision display
│       │   └── CAMReport.jsx     # CAM generation + HTML iframe + print
│       └── styles/
│           └── global.css        # Global styles
└── README.md
```

---

## 🇮🇳 Indian Context

This project is purpose-built for Indian corporate credit appraisal:

| Category | Details |
|----------|---------|
| **GST Compliance** | GSTR-1/3B/2A cross-verification, circular trading detection, ITC excess claims |
| **CIBIL** | Score model (300–900 range), minimum acceptable 650 |
| **Regulators** | MCA (ROC filing), NCLT (insolvency), RBI (base rate), SEBI, DRT, SFIO, DGGI |
| **Document Formats** | CIN, GSTIN, PAN regex validation; ₹ Crore/Lakhs parsing |
| **Rating Agencies** | CRISIL, ICRA, CARE, FITCH, India Ratings, Acuite |
| **Industry Risk** | Sector-specific mappings (NBFC liquidity, RERA, AGR dues, PLI scheme) |
| **Legal Framework** | Companies Act 2013, IBC, wilful defaulter circulars |

---

## 🤖 Does This Project Use ML?

### Short Answer

The project uses a **custom rule-based scoring engine** inspired by machine learning methodology, not trained ML models.

<details>
<summary><b>Detailed Explanation</b></summary>

| Aspect | Status |
|--------|--------|
| scikit-learn in requirements | ✅ Listed as dependency |
| Trained ML models (.pkl files) | ❌ None — `ml_models/` directory is empty |
| sklearn `fit()` / `predict()` calls | ❌ Not used anywhere in code |
| Feature engineering pipelines | ❌ No sklearn transformers |
| Neural networks / deep learning | ❌ Not used |

### What It Actually Uses: Explainable Rule-Based Scoring

Instead of a black-box ML model, the scoring engine uses a **deterministic point-based system** with full transparency:

1. **Base scores** — Each of the Five Cs starts with a base score (50–75)
2. **Point adjustments** — Financial metrics add/subtract points based on Indian banking benchmarks
   - EBITDA margin > 20% → +15 points, < 3% → -15 points
   - Debt-to-equity ≤ 0.5 → +20 points, > 3.0 → -20 points
   - Wilful defaulter flag → -50 points (automatic reject trigger)
3. **Score capping** — Each C is capped at 0–100
4. **Weighted aggregation** — Final score = weighted sum using Five Cs weights
5. **Decision logic** — Threshold-based loan decision with amount, rate, and tenure

### Why This Approach?

- **Explainability** — Every point change has a human-readable reason (critical for banking regulators)
- **Auditability** — Deterministic logic can be audited unlike black-box models
- **India-context** — Thresholds calibrated to Indian banking norms (RBI guidelines, CIBIL ranges)
- **Extensible** — Architecture supports swapping in real ML models later via the `ml_models/` directory

### ML-Ready Architecture

The codebase is structured to add real ML models:
- `ml_models/` directory exists for `.pkl` / `.joblib` model files
- `scikit-learn` and `joblib` are already in dependencies
- Scoring engine can be extended to use model predictions alongside rule-based scores
- Feature extraction from financial data is already structured as dictionaries (ready for DataFrame conversion)

</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for Hackathon** · Explainable AI · India-Context Credit Intelligence

Made with ❤️ for Indian Banking

</div>
