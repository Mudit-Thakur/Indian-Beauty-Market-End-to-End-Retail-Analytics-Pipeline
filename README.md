# 🛍️ Indian Beauty Market Analytics Dashboard

> End-to-end retail analytics pipeline — from raw data to boardroom-ready Power BI dashboards.

**Author:** Mudit Thakur &nbsp;|&nbsp; **Stack:** Python · Polars · DuckDB · Power BI · Parquet

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![DuckDB](https://img.shields.io/badge/DuckDB-SQL-FFC300?style=flat)](https://duckdb.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

![Dashboard Overview](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Overview.png)

---

## 📌 Project Summary

Simulates **50,000 transactions** across 1,000 customers and 10 beauty products in the Indian retail market. Demonstrates a complete analytics workflow — data generation, ETL, SQL analytics, customer segmentation, and interactive dashboards — delivering insights that directly inform marketing, inventory, and sales strategy.

> 📖 **[Data Dictionary](DATA_DICTIONARY.md)** — field definitions, generation logic, and synthetic data limitations  
> 📊 **[Executive Report](EXECUTIVE_REPORT.md)** — full KPI results with concrete numbers from the analysis

**Business hypotheses tested:**
- Do festival campaigns meaningfully lift revenue — and is it volume or ticket size driving the increase?
- Which products drive 80% of revenue (Pareto)?
- What percentage of the customer base is at risk of churning?
- Which customer tier drives disproportionate revenue?

---

## 📈 Key Results (FY 2024)

| Metric | Result |
|---|---|
| **Total Revenue** | ₹1,62,45,950 |
| **Average Order Value** | ₹324.92 |
| **Skincare Revenue Share** | 75.8% of total (₹1.23Cr) |
| **Top Product** | Sunscreen SPF50 — ₹30.3L (18.6% of revenue) |
| **Top 3 Products Revenue Share** | ~46% of total revenue |
| **Festival Revenue Contribution** | 19.9% of annual revenue across 3 festivals |
| **Festival AOV vs. Non-Festival** | ₹327 vs. ₹325 — volume drives lift, not ticket size |
| **At-Risk Customers** | 302 customers (30.2% of base) |
| **VIP + Loyal Revenue Share** | 94% of total revenue from 86% of customers |
| **Peak Month** | March 2024 — ₹21.9L (13.5%) driven by Holi |

---

## 📊 Dashboards

| Overview | Product Analysis |
|:---:|:---:|
| ![Overview](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Overview.png) | ![Product Analysis](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Product%20Analysis.png) |

| Customer & City Analytics | Festival Analytics |
|:---:|:---:|
| ![Customer & City Analytics](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Customer%20%26%20City%20Analytics.png) | ![Festival Analytics](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/screenshots/Festival%20Analysis.png) |

---

## 🔍 Analytics Modules

### 🛒 Product & Category Performance
- Pareto (80/20): top 3 SKUs = **~46% of revenue**; all 6 Skincare products = **75.8% of revenue**
- Skincare AOV (₹406) is 2.3× higher than Makeup AOV (₹175)
- Lowest revenue product: Lip Balm (₹149 price point, Makeup category)

### 👥 Customer Intelligence
- **RFM Segmentation** — Champions (206), Loyal (165), Potential Loyalists (327), At-Risk (302)
- **Cohort Retention** — month-over-month retention tracked from Jan–Dec 2024 acquisition cohorts
- **KPIs:** AOV ₹324.92 · Purchase Frequency 50 orders/customer · Revenue per Customer ₹16,246
- **Tiered Segmentation** — VIP (232) + Loyal (629) drive 94% of revenue

### 🎉 Festival Analytics
- Three festivals (Holi, Diwali, Summer) = **19.9% of revenue** (₹32.4L total)
- AOV is stable across all periods (~₹324–329) — festivals drive **volume, not spend-per-order**
- March peak (₹21.9L) is the single highest revenue month — 2× a typical non-festival month

### 🗺️ City-Level Intelligence
- 301 unique cities; revenue distributed evenly (max city share: 0.9%)
- Top city by revenue: South Dumdum (₹1.44L, 446 transactions)
- AOV consistent across cities (₹315–₹330 range)

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Generation | Python, Faker, NumPy, Pandas |
| Data Processing | **Polars** (fast, memory-efficient ETL) |
| Storage | CSV, Parquet |
| SQL Analytics | **DuckDB** (window functions, aggregations, joins on Parquet) |
| Visualization | **Power BI** (drill-down interactive dashboards) |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```
Indian-Beauty-Market-Analytics-Dashboard/
│
├── src/                                     # ← Modular production scripts
│   └── etl_pipeline.py                      # Data generation + cleaning pipeline
│
├── data/
│   ├── products.csv
│   ├── customers.csv
│   ├── transactions.csv
│   ├── sales_cleaned.csv / .parquet
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
│   ├── 03_day3_rfm_analysis.ipynb           # RFM scoring & segments
│   ├── 04_day4_cohort_retention.ipynb       # Cohort retention matrix
│   ├── 05_day5_customer_behavior.ipynb      # Behavioral KPIs
│   ├── 06_day6_product_performance.ipynb    # Pareto & product ranking
│   ├── 07_day7_festival_analysis.ipynb      # Festival revenue impact
│   ├── 08_day8_city_analysis.ipynb          # Geographic analytics
│   ├── 09_day9_sales_trends.ipynb           # Monthly trends & overlays
│   ├── 10_day10_customer_segmentation.ipynb # VIP/Loyal/Regular tiers
│   └── 11_day11_duckdb_analysis.ipynb       # SQL analytics on Parquet
│
├── screenshots and reports/
├── DATA_DICTIONARY.md                       # ← Field definitions & generation logic
├── EXECUTIVE_REPORT.md                      # ← Full KPI results with numbers
└── README.md
```

---

## ⚡ Quickstart

### Option A — Run modular ETL script (recommended)
```bash
git clone https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard.git
cd Indian-Beauty-Market-Analytics-Dashboard
pip install -r requirements.txt

# Generate synthetic data + run full ETL pipeline
python src/etl_pipeline.py

# Or: clean & join only (if raw CSVs already exist)
python src/etl_pipeline.py --clean
```

### Option B — Run notebooks sequentially
```bash
pip install -r requirements.txt
# Run notebooks in order: Day 1 → Day 11
# Each notebook builds on the output of the previous one.
```

> **Note:** Notebooks must be run in order. Day 1 generates the raw data; subsequent notebooks consume and enrich it.

---

## 📖 Documentation

| Document | Description |
|---|---|
| [DATA_DICTIONARY.md](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/data%20dict%20%26%20report/DATA_DICTIONARY.md) | All fields, data types, generation logic, and synthetic data limitations |
| [EXECUTIVE_REPORT.md](https://github.com/Mudit-Thakur/Indian-Beauty-Market-Analytics-Dashboard/blob/main/data%20dict%20%26%20report/EXECUTIVE_REPORT.md) | Full KPI results — products, customers, festivals, cities, RFM |

---

## 🔮 Roadmap

- [ ] Real-time dashboard via live sales API integration
- [ ] Demand forecasting with Prophet / XGBoost
- [ ] ML-based customer segmentation (K-Means / DBSCAN)
- [ ] Multi-category comparative dashboards

---

## 📬 Contact

**Mudit Thakur**  
[GitHub](https://github.com/Mudit-Thakur) · [Email](mailto:muditthakur918@gmail.com)
