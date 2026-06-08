import logging
import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from huggingface_hub import hf_hub_download
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="E-Commerce Product Intelligence Platform")

# HF Dataset config
HF_DATASET_ID = "Vincentran/ecommerce-dataset"
HF_CSV_PATH = "data/ecommerce_products.csv"

# Cache DataFrame
_data_cache = None


def load_data():
    """Load CSV từ HF Dataset with cache."""
    try:
        if _data_cache is not None:
            logger.info("Using cached DataFrame")
            return _data_cache

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

        # Cache DataFrame
        _data_cache = df
        return df

    except Exception as e:
        logger.error(f"Failed to load data from HF Dataset: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")


def refresh_cache():
    """Refresh data cache."""
    _data_cache = None
    return load_data()


@app.get("/")
def root():
    return {"status": "E-Commerce Product Intelligence API is running"}


@app.get("/data")
def get_data(
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(100, ge=1, le=500, description="Items per page")
):
    df = load_data()
    total = len(df)
    start = (page - 1) * limit
    end = start + limit

    if start >= total:
        raise HTTPException(status_code=404, detail="Page not found")

    data = df.iloc[start:end].to_dict("records")
    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit
    }


@app.get("/stats/categories")
def stats_categories():
    df = load_data()
    if "category" not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'category' column")
    return df["category"].value_counts().head(10).to_dict()


@app.get("/stats/brands")
def stats_brands():
    df = load_data()
    if "brand" not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'brand' column")
    return df["brand"].value_counts().head(10).to_dict()


@app.get("/stats/price")
def stats_price():
    df = load_data()
    if "category" not in df.columns or "price" not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'category' or 'price' column")
    return df.groupby("category")["price"].agg(["mean", "median", "min", "max", "count"]).reset_index().to_dict(
        "records")


@app.get("/stats/rating")
def stats_rating():
    df = load_data()
    if "category" not in df.columns or "rating" not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'category' or 'rating' column")
    return df.groupby("category")["rating"].agg(["mean", "median", "min", "max", "count"]).reset_index().to_dict(
        "records")


@app.get("/stats/price-range")
def stats_price_range():
    """Price distribution by range."""
    df = load_data()
    if "price" not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'price' column")

    price_ranges = {
        "Under $50": len(df[df["price"] < 50]),
        "$50 - $100": len(df[(df["price"] >= 50) & (df["price"] < 100)]),
        "$100 - $200": len(df[(df["price"] >= 100) & (df["price"] < 200)]),
        "$200 - $500": len(df[(df["price"] >= 200) & (df["price"] < 500)]),
        "$500+": len(df[df["price"] >= 500])
    }
    return price_ranges


@app.get("/insights")
def insights():
    df = load_data()
    return JSONResponse(content={
        "total_products": len(df),
        "categories": df["category"].nunique() if "category" in df.columns else 0,
        "brands": df["brand"].nunique() if "brand" in df.columns else 0,
        "avg_price": round(df["price"].mean(), 2) if "price" in df.columns else 0,
        "avg_rating": round(df["rating"].mean(), 2) if "rating" in df.columns else 0,
        "min_price": round(df["price"].min(), 2) if "price" in df.columns else 0,
        "max_price": round(df["price"].max(), 2) if "price" in df.columns else 0,
    })


@app.get("/search")
def search(
        query: str = Query(..., description="Search query"),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(100, ge=1, le=500, description="Items per page")
):
    df = load_data()
    q = query.lower()

    # Search only in important columns
    search_cols = ["product_name", "category", "brand", "description"]
    search_cols = [col for col in search_cols if col in df.columns]

    mask = pd.Series([False] * len(df), index=df.index)
    for col in search_cols:
        try:
            mask |= df[col].str.contains(q, case=False, na=False)
        except:
            pass

    total = len(df[mask])
    start = (page - 1) * limit
    end = start + limit

    if start >= total:
        raise HTTPException(status_code=404, detail="No results found")

    data = df[mask].iloc[start:end].to_dict("records")
    return {
        "data": data,
        "query": query,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit
    }


@app.get("/filter")
def filter_products(
        category: Optional[str] = Query(None, description="Filter by category"),
        min_price: Optional[float] = Query(None, description="Min price"),
        max_price: Optional[float] = Query(None, description="Max price"),
        min_rating: Optional[float] = Query(None, description="Min rating"),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(100, ge=1, le=500, description="Items per page")
):
    df = load_data()

    # Apply filters
    if category and "category" in df.columns:
        df = df[df["category"] == category]
    if min_price and "price" in df.columns:
        df = df[df["price"] >= min_price]
    if max_price and "price" in df.columns:
        df = df[df["price"] <= max_price]
    if min_rating and "rating" in df.columns:
        df = df[df["rating"] >= min_rating]

    total = len(df)
    start = (page - 1) * limit
    end = start + limit

    if start >= total:
        raise HTTPException(status_code=404, detail="No results found")

    data = df.iloc[start:end].to_dict("records")
    return {
        "data": data,
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "min_rating": min_rating
        },
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit
    }


@app.get("/recommend")
def recommend(category: str, limit: int = Query(10, ge=1, le=50, description="Number of recommendations")):
    df = load_data()
    if "category" not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'category' column")

    subset = df[df["category"] == category]
    if len(subset) == 0:
        raise HTTPException(status_code=404, detail="No products found in this category")

    if "rating" in df.columns:
        subset = subset.sort_values("rating", ascending=False)

    return subset.head(limit).to_dict("records")


@app.post("/refresh-data")
def refresh_data():
    """Refresh data cache from HF Dataset."""
    try:
        df = refresh_cache()
        return {"status": "Data refreshed successfully", "rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run-scraper")
def trigger_scraper():
    """Trigger download Kaggle → save CSV → upload to HF."""
    import subprocess
    result = subprocess.run(["python", "backend/scraper.py"], capture_output=True, text=True)
    if result.returncode == 0:
        # Refresh cache after scraper
        refresh_cache()
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