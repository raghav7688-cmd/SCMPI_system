import pandas as pd
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent / "datasets"


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


@lru_cache(maxsize=1)
def load_crop_data() -> pd.DataFrame:
    path = DATA_DIR / "district_season_crop.csv"
    df = pd.read_csv(path)
    df = df.rename(columns={"Suggested_Crop": "Crop", "Max_Production": "Production"})
    df = _coerce_numeric(df, ["Production", "Area", "Crop_Year"])
    for col in ["State_Name", "District_Name", "Season", "Crop"]:
        if col in df.columns:
            df[f"{col}_norm"] = df[col].map(normalize_text)
    df = df.dropna(subset=["State_Name", "District_Name", "Season", "Crop", "Production"])
    return df


@lru_cache(maxsize=1)
def load_mandi_data() -> pd.DataFrame:
    path = DATA_DIR / "crop_mandi_price.csv"
    df = pd.read_csv(path)
    numeric_cols = [col for col in df.columns if col.startswith("Price_") or col.startswith("Arrival_") or col == "MSP_2026_27"]
    df = _coerce_numeric(df, numeric_cols)
    if "Commodity" in df.columns:
        df["Commodity_norm"] = df["Commodity"].map(normalize_text)
    if "District" in df.columns:
        df["District_norm"] = df["District"].map(normalize_text)
    df = df.dropna(subset=["Commodity"])
    return df


@lru_cache(maxsize=1)
def load_state_supply_data() -> pd.DataFrame:
    path = DATA_DIR / "state_production_demand.csv"
    df = pd.read_csv(path)
    df = df.rename(
        columns={
            "TotalFoodgrains_2019_20": "Production",
            "Demand_Proxy_TotalFoodgrains_2017_18": "Demand",
        }
    )
    df = _coerce_numeric(df, ["Production", "Demand"])
    if "State" in df.columns:
        df["State_norm"] = df["State"].map(normalize_text)
    df = df.dropna(subset=["State", "Production", "Demand"])
    return df
