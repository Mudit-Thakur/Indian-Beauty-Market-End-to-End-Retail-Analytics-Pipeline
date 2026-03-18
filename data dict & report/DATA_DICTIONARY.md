# 📖 Data Dictionary — Indian Beauty Market Analytics

> All data is **synthetically generated** for portfolio purposes using Python (`Faker`, `NumPy`, `Pandas`).  
> No real customer or transaction data is used. Generation logic is documented below for full reproducibility.

---

## ⚙️ Why Synthetic Data?

Real Indian retail transaction data is proprietary and unavailable publicly. Synthetic generation allows:
- **Controlled realism** — Indian names, cities, festival calendar, and price points reflect actual market conditions
- **Full reproducibility** — anyone can regenerate the dataset from `01_day1_generate_code.ipynb`
- **Bias-free modeling** — RFM, cohort, and segmentation logic can be validated against known ground truth

**Trustworthiness note for reviewers:** The generation parameters (purchase probability distributions, festival windows, price tiers) were designed to reflect realistic Indian e-commerce patterns. Analytical results are valid for demonstrating methodology — not for drawing market-level conclusions.

---

## 🗂️ Tables

### 1. `products.csv` — Product Catalogue

| Field | Type | Description | Generation Logic |
|---|---|---|---|
| `product_id` | String | Unique product identifier (`p0`–`p9`) | Sequential index: `f"p{i}"` |
| `product_name` | String | Product name | Manually defined — 10 real Indian beauty products |
| `category` | String | Product category | Manually assigned: `Skincare`, `Haircare`, or `Makeup` |
| `price` | Integer (₹) | Fixed unit price | Manually set: ₹149–₹599 reflecting Indian market pricing |

**Products defined:**
| product_id | product_name | category | price (₹) |
|---|---|---|---|
| p0 | Aloe Vera Gel | Skincare | 299 |
| p1 | Vitamin C Serum | Skincare | 499 |
| p2 | Herbal Shampoo | Haircare | 199 |
| p3 | Lip Balm | Makeup | 149 |
| p4 | Face Wash | Skincare | 399 |
| p5 | Sunscreen SPF50 | Skincare | 599 |
| p6 | Hair Oil | Haircare | 249 |
| p7 | Body Lotion | Skincare | 349 |
| p8 | Nail Polish | Makeup | 199 |
| p9 | Face Pack | Skincare | 299 |

---

### 2. `customers.csv` — Customer Master

| Field | Type | Description | Generation Logic |
|---|---|---|---|
| `customer_id` | String | Unique customer identifier (`c0`–`c999`) | Sequential index: `f"c{i}"` |
| `name` | String | Customer full name | `Faker("en_IN").name()` — Indian locale names |
| `city` | String | Customer's city | `Faker("en_IN").city()` — Indian cities (301 unique cities in output) |
| `age` | Integer | Customer age | `random.randint(18, 55)` — uniform distribution |
| `gender` | String | Customer gender | `random.choice(["Male", "Female"])` — 50/50 split |

---

### 3. `transactions.csv` — Raw Transactions

| Field | Type | Description | Generation Logic |
|---|---|---|---|
| `transaction_id` | String | Unique transaction ID (`T0`–`T49999`) | Sequential index: `f"T{i}"` |
| `customer_id` | String | FK → customers | Random sample from customers_df |
| `product_id` | String | FK → products | Random sample from products_df |
| `purchase_date` | Datetime | Date of transaction | See festival logic below |
| `price` | Integer (₹) | Price paid | Inherited from product price (no discounts) |
| `city` | String | City of purchase | Inherited from sampled customer |
| `festival` | String / Null | Festival period if applicable | `None` (80%) or festival name (20%) |

**Festival Generation Logic:**
```
For each transaction:
  - 20% probability → festival purchase
    - Randomly select: Diwali (Oct 10–Nov 10), Holi (Mar 1–31), or Summer (May 1–Jun 30)
    - Purchase date = random date within that festival window
  - 80% probability → non-festival purchase
    - Purchase date = random date within 2024-01-01 to 2024-12-31
    - festival = None
```

---

### 4. `sales_cleaned.parquet` — Enriched Sales Master

Core analytical table. Result of joining transactions + products + customers, with `revenue` column added.

| Field | Type | Description |
|---|---|---|
| `transaction_id` | String | Unique transaction ID |
| `customer_id` | String | Customer identifier |
| `product_id` | String | Product identifier |
| `purchase_date` | Datetime | Parsed datetime |
| `festival` | String / Null | Festival tag |
| `city` | String | Customer city |
| `product_name` | String | Joined from products |
| `category` | String | Joined from products |
| `customer_name` | String | Joined from customers |
| `age` | Integer | Joined from customers |
| `gender` | String | Joined from customers |
| `price` | Integer (₹) | Product price |
| `revenue` | Integer (₹) | = `price` (alias; no discounts in synthetic data) |

---

### 5. `customer_rfm.parquet` — RFM Scores

| Field | Type | Description |
|---|---|---|
| `customer_id` | String | Customer identifier |
| `last_purchase` | Datetime | Most recent purchase date |
| `recency` | Integer | Days since last purchase (reference: 2024-12-31) |
| `frequency` | Integer | Total number of transactions |
| `monetary` | Integer (₹) | Total revenue spent |
| `r_score` | Integer | Recency rank score (dense rank) |
| `f_score` | Integer | Frequency rank score (dense rank) |
| `m_score` | Integer | Monetary rank score (dense rank) |
| `rfm_score` | Integer | `r_score + f_score + m_score` |
| `segment` | String | Champions / Loyal Customers / Potential Loyalists / At Risk |

**Segmentation thresholds:**
```
rfm_score >= 1500  → Champions
rfm_score >= 1000  → Loyal Customers
rfm_score >= 500   → Potential Loyalists
else               → At Risk
```

---

### 6. `cohort_retention.parquet` — Cohort Retention

| Field | Type | Description |
|---|---|---|
| `cohort_month` | Datetime | Month of customer's first purchase |
| `cohort_index` | Integer | Months since first purchase (0 = acquisition month) |
| `customers` | Integer | Active customers in that cohort × period |
| `cohort_size` | Integer | Total customers acquired in cohort_month |
| `retention_rate` | Float | `customers / cohort_size` (0.0–1.0) |

---

### 7. `product_performance.parquet` — Product Analytics

| Field | Type | Description |
|---|---|---|
| `product_id` | String | Product identifier |
| `product_name` | String | Product name |
| `category` | String | Category |
| `transactions` | Integer | Total transaction count |
| `total_revenue` | Integer (₹) | Sum of revenue |
| `avg_price` | Float (₹) | Average price per transaction |
| `revenue_share_pct` | Float | % of total revenue |
| `cumulative_revenue` | Integer (₹) | Cumulative revenue (sorted by revenue desc) |
| `cumulative_revenue_pct` | Float | Cumulative % — used for Pareto analysis |

---

### 8. `customer_level_metrics.parquet` — Customer KPIs

| Field | Type | Description |
|---|---|---|
| `customer_id` | String | Customer identifier |
| `total_orders` | Integer | Total purchase count |
| `total_spent` | Integer (₹) | Cumulative revenue |
| `avg_order_value` | Float (₹) | `total_spent / total_orders` |
| `first_purchase` | Datetime | First transaction date |
| `last_purchase` | Datetime | Most recent transaction date |
| `customer_lifetime_days` | Integer | `last_purchase - first_purchase` in days |
| `purchase_frequency` | Float | `total_orders / (customer_lifetime_days + 1)` |
| `customer_type` | String | VIP / Loyal / Regular / Low Value |

**Customer type thresholds:**
```
total_spent > 20,000  → VIP
total_orders >= 40    → Loyal
total_orders >= 15    → Regular
else                  → Low Value
```

---

### 9. `festival_sales.parquet` — Festival Analytics

| Field | Type | Description |
|---|---|---|
| `festival` | String / Null | Festival name or null (non-festival) |
| `transactions` | Integer | Transaction count |
| `total_revenue` | Integer (₹) | Revenue |
| `avg_order_value` | Float (₹) | Average order value |
| `revenue_share_pct` | Float | % of total revenue |

---

### 10. `city_performance.parquet` — City Analytics

| Field | Type | Description |
|---|---|---|
| `city` | String | City name |
| `transactions` | Integer | Transaction count |
| `total_revenue` | Integer (₹) | Total revenue |
| `average_order_value` | Float (₹) | AOV |
| `revenue_share_pct` | Float | % of total revenue |

---

### 11. `monthly_sales.parquet` — Sales Trends

| Field | Type | Description |
|---|---|---|
| `year_month` | String | Format: `YYYY-MM` |
| `transactions` | Integer | Monthly transaction count |
| `total_revenue` | Integer (₹) | Monthly revenue |
| `average_order_value` | Float (₹) | Monthly AOV |
| `revenue_share_pct` | Float | % of annual revenue |

---

## ⚠️ Known Synthetic Data Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Fixed product catalogue (10 SKUs) | No long-tail distribution | Sufficient for Pareto and category analysis |
| No repeat-customer purchase bias | All customers equally likely per transaction | RFM frequency patterns still valid; methodology demonstrated correctly |
| Revenue = price (no discounts/returns) | Overstates revenue vs. real retail | Clearly documented; metrics are directionally valid |
| Cities from Faker — not population-weighted | No metro/tier-2 bias in transaction distribution | Geographic analysis reflects uniform sampling, not real market share |
| Festival dates fixed (no year variation) | Cannot model year-over-year festival trends | Lift analysis within 2024 is valid |
