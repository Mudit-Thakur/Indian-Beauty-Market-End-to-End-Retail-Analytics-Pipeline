# Indian Beauty Market Analytics Dashboard

**End-to-end retail analytics pipeline** — synthetic data generation → ETL → SQL analytics → RFM segmentation → Power BI dashboards → **AI conversational analytics layer.**

**Stack:** Python · Polars · DuckDB · Power BI · Parquet · LangChain · Groq LLaMA 3.3

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.10-FFC300?style=flat)](https://duckdb.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![LangChain](https://img.shields.io/badge/LangChain-Agent-1C3C3C?style=flat)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-F55036?style=flat)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What This Project Does

Simulates a full FY 2024 analytics cycle for an Indian D2C beauty brand — 50,000 transactions, 1,000 customers, 10 SKUs across 301 cities. The pipeline answers four real business questions that a retail analyst or marketing team would actually be asked:

1. Do festival campaigns drive revenue through higher order volume or higher spend-per-order?
2. Which SKUs drive 80% of revenue, and what does that mean for inventory allocation?
3. What share of the customer base is at churn risk right now?
4. Which customer tier is responsible for disproportionate revenue — and how concentrated is that risk?

---

## Key Business Results (FY 2024)

| Business Question | Finding | Recommended Action |
|---|---|---|
| Festival revenue driver | Volume, not spend — AOV stable at ₹325–327 across all periods | Scale order acquisition campaigns during festivals, not discount depth |
| SKU concentration | Top 3 SKUs = 46% of revenue; Sunscreen SPF50 alone = 18.6% | Protect stock of top 3 SKUs; high stockout risk |
| Category dominance | Skincare = 75.8% of revenue; AOV ₹406 vs. Makeup ₹175 | Prioritize skincare line expansion over makeup |
| Churn risk | 302 customers (30.2% of base) classified At-Risk | Activate win-back campaign immediately |
| Revenue concentration | VIP + Loyal tier = 94% of revenue from 86% of customers | High concentration risk — diversify loyalty base |
| Peak month | March 2024 = ₹21.9L — 2× a typical month, Holi-driven | Pre-load inventory and ad spend by mid-February |

**Total FY 2024 Revenue:** ₹1,62,45,950 &nbsp;|&nbsp; **AOV:** ₹324.92 &nbsp;|&nbsp; **Repeat Purchase Rate:** 48%

---

## 🤖 AI Analytics Agent

Built a conversational AI layer on top of this pipeline — non-technical stakeholders can query the entire dataset in plain English without writing a single line of SQL.

### Demo

![AI Agent Demo](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/raw/main/screenshots/ai_agent_demo.png)

### How It Works
```
User asks plain English question
        ↓
LangChain + Groq LLaMA 3.3 converts to SQL
        ↓
DuckDB executes query on Parquet files
        ↓
LLM explains results in business language
        ↓
Conversation memory retains last 5 exchanges
        ↓
Chat history auto-saved to log file
```

### Key Features

- **Natural language to SQL** — no technical knowledge needed
- **Conversation memory** — remembers last 5 questions for context-aware follow-ups
- **Business insights** — every result explained in plain English with recommendations
- **Chat history logging** — all sessions automatically saved to file
- **DuckDB + Parquet** — sub-second query responses on 50,000 transactions

### Run The AI Agent
```bash
# Install additional dependencies
pip install langchain langchain-community langchain-groq python-dotenv

# Set up environment variables
cp ai_agent/.env.example ai_agent/.env
# Add your Groq API key to .env file

# Run the agent
python ai_agent/beauty_agent.py
```

---

## Dashboards

![Overview](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Overview.png)

| Product Analysis | Customer & City Analytics |
|:---:|:---:|
| ![Product Analysis](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Product%20Analysis.png) | ![Customer & City Analytics](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Customer%20%26%20City%20Analytics.png) |

| Festival Analytics | |
|:---:|:---:|
| ![Festival Analytics](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Festival%20Analysis.png) | |

---

## Pipeline Architecture
```
Raw Data Generation (Python + Faker + NumPy)
        │
        ▼
ETL & Schema Validation (Polars)
        │
        ▼
Parquet Storage (columnar, query-optimized)
        │
        ▼
SQL Analytics (DuckDB — window functions, CTEs, aggregations)
        │
        ├── Product & Pareto Analysis
        ├── RFM Segmentation (Champions / Loyal / At-Risk)
        ├── Cohort Retention Matrix
        ├── Festival Revenue Attribution
        └── City-Level Geographic Analysis
                │
                ├── Power BI Dashboards (drill-down, cross-filtered)
                │
                └── AI Analytics Agent (LangChain + Groq + DuckDB)
                        └── Plain English Q&A → Business Insights
```

---

## Analytics Modules

### Product & Category Performance
- Top 3 SKUs = ~46% of revenue (Pareto confirmed)
- Skincare AOV (₹406) is 2.3× Makeup AOV (₹175) — not just volume, but spend-per-order differs by category
- Lowest-revenue SKU: Lip Balm at ₹149 — candidate for discontinuation or repositioning

### RFM Customer Segmentation
- **Champions:** 206 customers — highest recency, frequency, and spend
- **Loyal:** 165 customers — consistent purchasers, lower recency
- **Potential Loyalists:** 327 customers — recent but low frequency
- **At-Risk:** 302 customers (30.2%) — haven't purchased recently; win-back window closing
- VIP (232) + Loyal (629) tiers combined = 94% of total revenue

### Cohort Retention
- Month-over-month retention tracked across all 12 acquisition cohorts (Jan–Dec 2024)
- Identifies which acquisition months produce the stickiest customers

### Festival Revenue Attribution
- Holi + Diwali + Summer Sale = 19.9% of annual revenue (₹32.4L)
- Key insight: AOV holds flat (~₹324–329) across festival and non-festival periods — lift is purely transactional volume
- March 2024 is the single highest month at ₹21.9L (13.5% of annual revenue)

### City-Level Analysis
- 301 cities covered; no single city exceeds 0.9% revenue share — geographically distributed demand
- Top city: South Dumdum — ₹1.44L, 446 transactions
- AOV is consistent across geographies (₹315–₹330) — pricing strategy is working uniformly

---

## Tech Stack

| Layer | Tool | Why This Choice |
|---|---|---|
| Data Generation | Python, Faker, NumPy | Reproducible synthetic data with realistic distributions |
| ETL & Cleaning | **Polars** | 5–10× faster than Pandas for large DataFrames; memory-efficient |
| Storage | Parquet | Columnar format; DuckDB reads it 10× faster than CSV |
| SQL Analytics | **DuckDB** | Runs analytical SQL directly on Parquet files — no database server needed |
| Visualization | **Power BI** | Industry-standard BI tool; drill-through + cross-filter support |
| AI Agent | **LangChain + Groq** | Natural language to SQL with business insight generation |
| Version Control | Git & GitHub | Full commit history, reproducibility |

---

## Project Structure
```
Indian-Beauty-Market-Analytics-Dashboard/
│
├── ai_agent/
│   ├── beauty_agent.py           # AI analytics agent
│   └── .env.example              # API key template
│
├── pipelines/
│   └── etl_pipeline.py           # Full data generation + ETL pipeline
│
├── scripts/                      # Utility and helper scripts
│
├── data/
│   ├── products.csv
│   ├── customers.csv
│   ├── transactions.csv
│   ├── sales_cleaned.csv
│   ├── sales_cleaned.parquet
│   ├── customer_rfm.parquet
│   ├── cohort_retention.parquet
│   ├── customer_level_metrics.parquet
│   ├── product_performance.parquet
│   ├── category_performance.parquet
│   ├── city_performance.parquet
│   ├── festival_sales.parquet
│   └── monthly_sales.parquet
│
├── notebooks/
│   ├── 01_day1_generate_code.ipynb
│   ├── 02_day2_data_cleaning.ipynb
│   ├── 03_day3_rfm_analysis.ipynb
│   ├── 04_day4_cohort_retention.ipynb
│   ├── 05_day5_customer_behavior.ipynb
│   ├── 06_day6_product_performance.ipynb
│   ├── 07_day7_festival_analysis.ipynb
│   ├── 08_day8_city_analysis.ipynb
│   ├── 09_day9_sales_trends.ipynb
│   ├── 10_day10_customer_segmentation.ipynb
│   └── 11_day11_duckdb_analysis.ipynb
│
├── dashboard/
├── data dict & report/
│   ├── DATA_DICTIONARY.md
│   └── EXECUTIVE_REPORT.md
├── screenshots/
│   └── ai_agent_demo.png
├── requirements.txt
└── README.md
```

---

## Quickstart

**Prerequisites:** Python 3.10+, pip
```bash
# 1. Clone the repo
git clone https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard.git
cd Indian-Beauty-Market-Analytics-Dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3a. Run full pipeline (data generation + ETL)
python pipelines/etl_pipeline.py

# 3b. Or run ETL only (if raw CSVs already exist)
python pipelines/etl_pipeline.py --clean

# 4. Run AI agent
python ai_agent/beauty_agent.py
```

**To explore interactively:** Run notebooks in order (01 → 11). Each notebook depends on outputs from the previous one.

**To view dashboards:** Open `dashboard/*.pbix` in Power BI Desktop.

---

## Documentation

| Document | Contents |
|---|---|
| [DATA_DICTIONARY.md](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/data%20dict%20%26%20report/DATA_DICTIONARY.md) | All fields, data types, generation logic, and synthetic data limitations |
| [EXECUTIVE_REPORT.md](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/data%20dict%20%26%20report/EXECUTIVE_REPORT.md) | Full KPI breakdown — products, customers, festivals, cities, RFM |

---

## Skills Demonstrated

- **ETL pipeline design** — modular, parameterized, production-style Python scripts
- **Analytical SQL** — window functions, CTEs, aggregations, multi-table joins via DuckDB
- **Customer analytics** — RFM scoring, cohort retention, churn identification
- **AI analytics agent** — LangChain + Groq LLaMA 3.3 natural language to SQL
- **Conversation memory** — context-aware multi-turn analytics conversations
- **Business communication** — every metric tied to a decision or recommended action
- **Modern data stack** — Polars + DuckDB + Parquet + LangChain
- **BI dashboarding** — drill-through, cross-filtering, executive-level layout in Power BI

---

## Roadmap

- [x] AI conversational analytics agent
- [ ] Demand forecasting with Prophet or XGBoost
- [ ] ML-based customer clustering (K-Means / DBSCAN)
- [ ] Multi-category comparative dashboards
- [ ] Live sales API integration for real-time dashboard refresh

---

## Contact

**Mudit Thakur**
[GitHub](https://github.com/Mudit-Thakur) · [Email](mailto:muditthakur918@gmail.com)
