import pandas as pd

def generate_insights(df: pd.DataFrame):
    return {
        "total_products": len(df),
        "categories": df["category"].nunique(),
        "brands": df["brand"].nunique(),
        "avg_price": df["price"].mean(),
        "avg_rating": df["rating"].mean(),
    }

def semantic_search(query: str, df: pd.DataFrame):
    q = query.lower()
    mask = (
        df["title"].str.contains(q, case=False, na=False) |
        df["description"].str.contains(q, case=False, na=False)
    )
    return df[mask].head(100)

def recommend_by_category(df: pd.DataFrame, category: str):
    subset = df[df["category"] == category]
    return subset.sort_values("rating", ascending=False).head(10)