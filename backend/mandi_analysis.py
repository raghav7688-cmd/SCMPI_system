import re
from datetime import datetime
import pandas as pd

from .dataset_loader import load_mandi_data


def _parse_price_date(column_name: str) -> datetime:
    match = re.match(r"^Price_(\d{1,2}[A-Za-z]{3}\d{4})$", column_name)
    if not match:
        return datetime.min
    return datetime.strptime(match.group(1), "%d%b%Y")


def get_sorted_price_columns(df: pd.DataFrame) -> list[str]:
    return sorted([col for col in df.columns if col.startswith("Price_")], key=_parse_price_date)


def get_crop_price_estimate(crop: str) -> dict:
    df = load_mandi_data()
    filtered = df[df["Commodity_norm"] == crop.strip().lower()]
    if filtered.empty:
        return {
            "crop": crop.strip(),
            "estimated_price": None,
            "latest_price_column": None,
            "label": "crop-based estimate",
        }

    price_cols = get_sorted_price_columns(filtered)
    latest_price_col = price_cols[-1] if price_cols else None
    estimated_price = None

    if latest_price_col:
        latest_series = filtered[latest_price_col].dropna()
        if not latest_series.empty:
            estimated_price = round(float(latest_series.mean()), 2)

    return {
        "crop": str(filtered.iloc[0]["Commodity"]).strip(),
        "estimated_price": estimated_price,
        "latest_price_column": latest_price_col,
        "label": "crop-based estimate",
    }
