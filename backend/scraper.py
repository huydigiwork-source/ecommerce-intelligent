import os
import logging
import pandas as pd
from pathlib import Path
import shutil

# Set Kaggle env vars TRƯỚC khi import Kaggle
token = os.getenv("KAGGLE_API_TOKEN")
if token:
    token_value = token.split('_')[1] if '_' in token else token
    os.environ['KAGGLE_KEY'] = token_value
    os.environ['KAGGLE_USERNAME'] = 'johnsontrann'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATASET_SLUG = "anujsaha0123456789/e-commerce-product-intelligence-dataset"
TEMP_DIR = Path("data/temp_kaggle")
OUTPUT_CSV = Path("data/ecommerce_products.csv")

os.makedirs("data", exist_ok=True)


def setup_kaggle_api():
    """Auth Kaggle API."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    return api


def download_dataset():
    """Download dataset từ Kaggle."""
    api = setup_kaggle_api()
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading dataset: {DATASET_SLUG}")
    api.dataset_download_files(DATASET_SLUG, path=str(TEMP_DIR), unzip=True)
    logger.info("Download complete.")
    return TEMP_DIR


def find_csv_files(temp_dir: Path):
    """Tìm tất CSV files."""
    csv_files = list(temp_dir.glob("**/*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found.")
    return csv_files


def load_and_concatenate(csv_files):
    """Concatenate tất CSVs."""
    dfs = []
    for f in csv_files:
        logger.info(f"Loading: {f}")
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def save_csv(df: pd.DataFrame):
    """Save to CSV."""
    df.to_csv(OUTPUT_CSV, index=False)
    logger.info(f"Saved to: {OUTPUT_CSV}")


def run_scraper():
    """Full pipeline: download Kaggle → save CSV (không upload HF)."""
    try:
        download_dataset()
        csv_files = find_csv_files(TEMP_DIR)
        df = load_and_concatenate(csv_files)
        save_csv(df)
    finally:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

    return df


if __name__ == "__main__":
    run_scraper()