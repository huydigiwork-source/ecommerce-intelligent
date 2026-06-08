import logging
import os
import pandas as pd
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from huggingface_hub import hf_hub_download

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="E-Commerce Product Intelligence Platform")

# HF Dataset config
HF_DATASET_ID = "Vincentran/ecommerce-dataset"
HF_CSV_PATH = "data/ecommerce_products.csv"


def load_data():
    """Load CSV từ HF Dataset."""
    try:
        # Download CSV từ HF Dataset
        logger.info(f"Downloading CSV from HF Dataset: {HF_DATASET_ID}/{HF_CSV_PATH}")
        local_csv_path = hf_hub_download(
            repo_id=HF_DATASET_ID,
            filename=HF_CSV_PATH,
            repo_type="dataset"
        )

        file_size = os.path.getsize(local_csv_path)
        logger.info(f"Loading CSV from: {local_csv_path} (size: {file_size} bytes)")

        if file_size == 0:
            raise ValueError(f"CSV file is empty: {local_csv_path}")

        df = pd.read_csv(local_csv_path)
        logger.info(f"Loaded {len(df)} rows, columns: {list(df.columns)}")
        return df

    except Exception as e:
        logger.error(f"Failed to load data from HF Dataset: {e}")
        raise


@app.get("/")
def root():
    return {"status": "E-Commerce Product Intelligence API is running"}


@app.get("/data")
def get_data():
    df = load_data()
    return df.head(200).to_dict("records")


@app.get("/stats/categories")
def stats_categories():
    df = load_data()
    if "category" not in df.columns:
        raise ValueError("Missing 'category' column")
    return df["category"].value_counts().head(10).to_dict()


@app.get("/stats/brands")
def stats_brands():
    df = load_data()
    if "brand" not in df.columns:
        raise ValueError("Missing 'brand' column")
    return df["brand"].value_counts().head(10).to_dict()


@app.get("/stats/price")
def stats_price():
    df = load_data()
    if "category" not in df.columns or "price" not in df.columns:
        raise ValueError("Missing 'category' or 'price' column")
    return df.groupby("category")["price"].agg(["mean", "median", "min", "max", "count"]).reset_index().to_dict(
        "records")


@app.get("/stats/rating")
def stats_rating():
    df = load_data()
    if "category" not in df.columns or "rating" not in df.columns:
        raise ValueError("Missing 'category' or 'rating' column")
    return df.groupby("category")["rating"].agg(["mean", "median", "min", "max", "count"]).reset_index().to_dict(
        "records")


@app.get("/insights")
def insights():
    df = load_data()
    return JSONResponse(content={
        "total_products": len(df),
        "categories": df["category"].nunique() if "category" in df.columns else 0,
        "brands": df["brand"].nunique() if "brand" in df.columns else 0,
        "avg_price": df["price"].mean() if "price" in df.columns else 0,
        "avg_rating": df["rating"].mean() if "rating" in df.columns else 0,
    })


@app.get("/search")
def search(query: str):
    df = load_data()
    q = query.lower()

    # Find text columns
    text_cols = df.select_dtypes(include=["object"]).columns.tolist()

    mask = pd.Series([False] * len(df), index=df.index)
    for col in text_cols[:5]:  # Check first 5 text columns
        try:
            mask |= df[col].str.contains(q, case=False, na=False)
        except:
            pass

    return df[mask].head(100).to_dict("records")


@app.get("/recommend")
def recommend(category: str):
    df = load_data()
    if "category" not in df.columns:
        raise ValueError("Missing 'category' column")

    subset = df[df["category"] == category]
    if "rating" in df.columns:
        return subset.sort_values("rating", ascending=False).head(10).to_dict("records")
    return subset.head(10).to_dict("records")


@app.post("/run-scraper")
def trigger_scraper():
    """Trigger download Kaggle → save CSV → upload to HF."""
    import subprocess
    result = subprocess.run(["python", "backend/scraper.py"], capture_output=True, text=True)
    if result.returncode == 0:
        return {"status": "Scraper completed successfully", "output": result.stdout}
    else:
        return {"status": "Scraper failed", "error": result.stderr}


# Mount frontend
frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    @app.get("/")
    def frontend_placeholder():
        return HTMLResponse(
            content="<h1>E-Commerce Product Intelligence Dashboard</h1><p>Frontend placeholder.</p>"
        )