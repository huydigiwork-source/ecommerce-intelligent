import pandas as pd
from pathlib import Path

PARQUET_PATH = Path("data/ecommerce_products.parquet")

def load_data():
    """Load parquet."""
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(f"Parquet not found: {PARQUET_PATH}")
    return pd.read_parquet(PARQUET_PATH)

def get_top_categories(df: pd.DataFrame, n: int = 10):
    return df["category"].value_counts().head(n)

def get_top_brands(df: pd.DataFrame, n: int = 10):
    return df["brand"].value_counts().head(n)

def get_price_stats(df: pd.DataFrame):
    return df.groupby("category")["price"].agg(["mean", "median", "min", "max", "count"]).reset_index()

def get_rating_stats(df: pd.DataFrame):
    return df.groupby("category")["rating"].agg(["mean", "median", "min", "max", "count"]).reset_index()