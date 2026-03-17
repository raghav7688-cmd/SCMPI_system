import pandas as pd
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent / "datasets"


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@lru_cache(maxsize=1)
def load_crop_data() -> pd.DataFrame:
    path = DATA_DIR / "district_season_crop.csv"
    df = pd.read_csv(path)
    df = _coerce_numeric(df, ["Max_Production", "Crop_Year"])
    df = df.dropna()
    return df


@lru_cache(maxsize=1)
def load_mandi_data() -> pd.DataFrame:
    path = DATA_DIR / "crop_mandi_price.csv"
    df = pd.read_csv(path)
    numeric_cols = [col for col in df.columns if col.startswith("Price_") or col.startswith("Arrival_") or col == "MSP_2026_27"]
    df = _coerce_numeric(df, numeric_cols)
    df = df.dropna()
    return df


@lru_cache(maxsize=1)
def load_state_supply_data() -> pd.DataFrame:
    path = DATA_DIR / "state_production_demand.csv"
    df = pd.read_csv(path)
    df = _coerce_numeric(df, ["Production_TotalFoodgrains", "Demand_Proxy_TotalFoodgrains"])
    df = df.dropna()
    return df