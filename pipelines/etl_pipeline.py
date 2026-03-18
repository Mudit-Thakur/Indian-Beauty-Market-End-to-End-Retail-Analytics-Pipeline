"""
etl_pipeline.py
---------------
Modular ETL pipeline for the Indian Beauty Market Analytics project.
Replaces notebook-based ETL (Day 1 – Day 2) with production-style scripts.

Usage:
    python etl_pipeline.py --generate   # Generate synthetic data
    python etl_pipeline.py --clean      # Run cleaning & joins only
    python etl_pipeline.py              # Run full pipeline (generate + clean)
"""

import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from faker import Faker

# ── Config ────────────────────────────────────────────────────────────────────

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

NUM_CUSTOMERS = 1000
NUM_TRANSACTIONS = 50_000
RANDOM_SEED = 42

PRODUCTS = [
    ("Aloe Vera Gel",    "Skincare",  299),
    ("Vitamin C Serum",  "Skincare",  499),
    ("Herbal Shampoo",   "Haircare",  199),
    ("Lip Balm",         "Makeup",    149),
    ("Face Wash",        "Skincare",  399),
    ("Sunscreen SPF50",  "Skincare",  599),
    ("Hair Oil",         "Haircare",  249),
    ("Body Lotion",      "Skincare",  349),
    ("Nail Polish",      "Makeup",    199),
    ("Face Pack",        "Skincare",  299),
]

FESTIVALS = {
    "Diwali": ("2024-10-10", "2024-11-10"),
    "Holi":   ("2024-03-01", "2024-03-31"),
    "Summer": ("2024-05-01", "2024-06-30"),
}

FESTIVAL_PROBABILITY = 0.20  # 20% of transactions occur during a festival


# ── Helpers ───────────────────────────────────────────────────────────────────

def random_date(start: str, end: str) -> pd.Timestamp:
    """Return a random date between start and end (inclusive)."""
    return pd.to_datetime(
        np.random.choice(pd.date_range(start, end))
    )


# ── Generation ────────────────────────────────────────────────────────────────

def generate_products() -> pl.DataFrame:
    """Generate the 10-product catalogue."""
    records = [
        {"product_id": f"p{i}", "product_name": name, "category": cat, "price": price}
        for i, (name, cat, price) in enumerate(PRODUCTS)
    ]
    df = pl.DataFrame(records)
    df.write_csv(DATA_DIR / "products.csv")
    print(f"✅ products.csv — {len(df)} rows")
    return df


def generate_customers() -> pl.DataFrame:
    """Generate 1,000 synthetic Indian customers."""
    faker = Faker("en_IN")
    random.seed(RANDOM_SEED)

    records = [
        {
            "customer_id": f"c{i}",
            "name":        faker.name(),
            "city":        faker.city(),
            "age":         random.randint(18, 55),
            "gender":      random.choice(["Male", "Female"]),
        }
        for i in range(NUM_CUSTOMERS)
    ]
    df = pl.DataFrame(records)
    df.write_csv(DATA_DIR / "customers.csv")
    print(f"✅ customers.csv — {len(df)} rows")
    return df


def generate_transactions(
    products_df: pl.DataFrame,
    customers_df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Generate 50,000 transactions.

    Festival logic:
        - 20% probability → festival purchase (random festival, random date within window)
        - 80% probability → non-festival purchase (random date within full year)
    """
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)

    festival_names = list(FESTIVALS.keys())
    records = []

    for i in range(NUM_TRANSACTIONS):
        customer = customers_df.sample(1).to_dict(as_series=False)
        product  = products_df.sample(1).to_dict(as_series=False)

        if random.random() < FESTIVAL_PROBABILITY:
            fest = random.choice(festival_names)
            purchase_date = random_date(*FESTIVALS[fest])
            festival = fest
        else:
            purchase_date = random_date("2024-01-01", "2024-12-31")
            festival = None

        records.append({
            "transaction_id": f"T{i}",
            "customer_id":    customer["customer_id"][0],
            "product_id":     product["product_id"][0],
            "purchase_date":  purchase_date,
            "price":          product["price"][0],
            "city":           customer["city"][0],
            "festival":       festival,
        })

    df = pl.DataFrame(records).with_columns(
        pl.col("purchase_date").cast(pl.Datetime)
    )
    df.write_csv(DATA_DIR / "transactions.csv")
    print(f"✅ transactions.csv — {len(df)} rows")
    return df


# ── Cleaning & Joining ────────────────────────────────────────────────────────

def load_raw() -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """Load raw CSVs from disk."""
    transactions_df = pl.read_csv(DATA_DIR / "transactions.csv").with_columns(
        pl.col("purchase_date").str.to_datetime()
    )
    products_df  = pl.read_csv(DATA_DIR / "products.csv")
    customers_df = pl.read_csv(DATA_DIR / "customers.csv")
    return transactions_df, products_df, customers_df


def validate(df: pl.DataFrame, name: str) -> None:
    """Assert no null values in critical columns and print shape."""
    nulls = df.null_count().to_dict(as_series=False)
    total_nulls = sum(v[0] for v in nulls.values())
    if total_nulls > 0:
        raise ValueError(f"❌ {name} has {total_nulls} null values: {nulls}")
    print(f"✅ {name} validated — shape: {df.shape}")


def clean_and_join(
    transactions_df: pl.DataFrame,
    products_df: pl.DataFrame,
    customers_df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Join transactions → products → customers.
    Add revenue column.
    Reorder and rename for analytics readability.
    """
    sales_df = (
        transactions_df
        .join(products_df, on="product_id", how="left")
        .join(customers_df, on="customer_id", how="left")
        .rename({"name": "customer_name"})
        .with_columns(pl.col("price").alias("revenue"))
        .select([
            "transaction_id", "customer_id", "product_id",
            "purchase_date", "festival", "city",
            "product_name", "category",
            "customer_name", "age", "gender",
            "price", "revenue",
        ])
        .sort("purchase_date")
    )

    validate(sales_df.select(["transaction_id", "customer_id", "product_id",
                               "purchase_date", "price", "revenue"]),
             "sales_df")

    sales_df.write_csv(DATA_DIR / "sales_cleaned.csv")
    sales_df.write_parquet(DATA_DIR / "sales_cleaned.parquet")
    print(f"✅ sales_cleaned.parquet saved — {len(sales_df):,} rows, {len(sales_df.columns)} columns")
    return sales_df


# ── Orchestrator ──────────────────────────────────────────────────────────────

def run_pipeline(generate: bool = True) -> pl.DataFrame:
    """
    Full ETL orchestration.

    Args:
        generate: If True, regenerate synthetic raw data.
                  If False, load existing CSVs from DATA_DIR.
    """
    print("\n── ETL Pipeline ─────────────────────────────────────────")

    if generate:
        print("\n[1/3] Generating synthetic data...")
        products_df  = generate_products()
        customers_df = generate_customers()
        _            = generate_transactions(products_df, customers_df)

    print("\n[2/3] Loading raw data...")
    transactions_df, products_df, customers_df = load_raw()

    print("\n[3/3] Cleaning and joining...")
    sales_df = clean_and_join(transactions_df, products_df, customers_df)

    print("\n── Pipeline complete ────────────────────────────────────\n")
    return sales_df


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indian Beauty Market ETL Pipeline")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Regenerate synthetic raw data (products, customers, transactions)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Run cleaning & joining only (requires existing CSVs in data/)",
    )
    args = parser.parse_args()

    if args.clean:
        run_pipeline(generate=False)
    else:
        run_pipeline(generate=True)
