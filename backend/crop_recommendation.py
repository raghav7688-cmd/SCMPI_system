import pandas as pd
from .dataset_loader import load_crop_data


def recommend_crop(state: str, season: str) -> dict:
    df = load_crop_data()
    filtered = df[(df["State_Name"].str.lower() == state.lower()) & (df["Season"].str.lower() == season.lower())]
    if filtered.empty:
        return {"recommended_crop": None, "expected_production": 0, "confidence": 0.0}

    grouped = filtered.groupby("Suggested_Crop")["Max_Production"].sum().sort_values(ascending=False)
    top_crop = grouped.index[0]
    production = float(grouped.iloc[0])
    confidence = min(0.95, production / grouped.sum()) if grouped.sum() else 0.0

    return {
        "recommended_crop": top_crop,
        "expected_production": round(production, 2),
        "confidence": round(confidence, 2),
    }