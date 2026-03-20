# Indian Beauty Market Analytics Dashboard

**End-to-end retail analytics pipeline** — synthetic data generation → ETL → SQL analytics → RFM segmentation → Power BI dashboards.

**Stack:** Python · Polars · DuckDB · Power BI · Parquet · Faker

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.10-FFC300?style=flat)](https://duckdb.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
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
                ▼
        Power BI Dashboards (drill-down, cross-filtered)
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
| Version Control | Git & GitHub | Full commit history, reproducibility |

---

## Project Structure

```
Indian-Beauty-Market-Analytics-Dashboard/
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
│   ├── 01_day1_generate_code.ipynb          # Synthetic data generation
│   ├── 02_day2_data_cleaning.ipynb          # ETL & schema validation
│   ├── 03_day3_rfm_analysis.ipynb           # RFM scoring & segmentation
│   ├── 04_day4_cohort_retention.ipynb       # Cohort retention matrix
│   ├── 05_day5_customer_behavior.ipynb      # Behavioral KPIs
│   ├── 06_day6_product_performance.ipynb    # Pareto & SKU ranking
│   ├── 07_day7_festival_analysis.ipynb      # Festival revenue impact
│   ├── 08_day8_city_analysis.ipynb          # Geographic analytics
│   ├── 09_day9_sales_trends.ipynb           # Monthly trends & seasonality
│   ├── 10_day10_customer_segmentation.ipynb # VIP / Loyal / Regular tiering
│   └── 11_day11_duckdb_analysis.ipynb       # SQL analytics on Parquet
│
├── dashboard/                    # Power BI .pbix file
│
├── data dict & report/
│   ├── DATA_DICTIONARY.md        # Field definitions, generation logic, synthetic data limitations
│   └── EXECUTIVE_REPORT.md       # Full KPI results with numbers
│
├── screenshots/
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
```

**To explore interactively:** Run notebooks in order (01 → 11). Each notebook depends on outputs from the previous one.

**To view dashboards:** Open `dashboard/*.pbix` in Power BI Desktop (free download at powerbi.microsoft.com).

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
- **Business communication** — every metric tied to a decision or recommended action
- **Modern data stack** — Polars + DuckDB + Parquet (the stack replacing Pandas + SQL Server in 2024–2025)
- **BI dashboarding** — drill-through, cross-filtering, executive-level layout in Power BI

---

## Roadmap

- [ ] Demand forecasting with Prophet or XGBoost
- [ ] ML-based customer clustering (K-Means / DBSCAN) to validate RFM segments
- [ ] Multi-category comparative dashboards (Beauty vs. Personal Care vs. Wellness)
- [ ] Live sales API integration for real-time dashboard refresh

---

## Contact

**Mudit Thakur**  
[GitHub](https://github.com/Mudit-Thakur) · [Email](mailto:muditthakur918@gmail.com)
