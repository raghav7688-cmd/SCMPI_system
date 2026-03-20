import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .dataset_loader import load_crop_data

MODEL_PATH = Path(__file__).parent / "model.joblib"
REQUIRED_MODEL_FEATURES = {"State_Name", "District_Name", "Season", "Crop", "Crop_Year"}


def build_pipeline(df: pd.DataFrame) -> Pipeline:
    df = df.copy()
    area_col = "Area" if "Area" in df.columns else None

    features = ["State_Name", "District_Name", "Season", "Crop", "Crop_Year"] + ([area_col] if area_col else [])
    X = df[features]
    y = df["Production"]

    categorical = ["State_Name", "District_Name", "Season", "Crop"]
    numeric = ["Crop_Year"] + ([area_col] if area_col else [])

    preprocessor = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    model = RandomForestRegressor(n_estimators=120, random_state=42)

    return Pipeline([
        ("preprocess", preprocessor),
        ("model", model),
    ])


def train_and_save() -> dict:
    df = load_crop_data().copy()
    pipe = build_pipeline(df)

    area_col = "Area" if "Area" in df.columns else None
    feature_cols = ["State_Name", "District_Name", "Season", "Crop", "Crop_Year"] + ([area_col] if area_col else [])

    X = df[feature_cols]
    y = df["Production"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    score = r2_score(y_test, preds)
    joblib.dump(pipe, MODEL_PATH)
    return {"r2": round(score, 3), "path": str(MODEL_PATH)}


def load_model() -> Pipeline:
    if not MODEL_PATH.exists():
        train_and_save()

    model = joblib.load(MODEL_PATH)
    model_features = set(getattr(model, "feature_names_in_", []))
    if not REQUIRED_MODEL_FEATURES.issubset(model_features):
        train_and_save()
        model = joblib.load(MODEL_PATH)
    return model


def predict_yield(state: str, district: str, season: str, crop: str, area: float) -> dict:
    model = load_model()
    input_row = {
        "State_Name": state,
        "District_Name": district,
        "Season": season,
        "Crop": crop,
        "Crop_Year": 2025,
    }
    if "Area" in model.feature_names_in_:
        input_row["Area"] = area
    df = pd.DataFrame([input_row])
    pred = float(model.predict(df)[0])

    if hasattr(model.named_steps["model"], "estimators_"):
        transformed = model.named_steps["preprocess"].transform(df)
        est_preds = np.vstack([tree.predict(transformed) for tree in model.named_steps["model"].estimators_])
        std = est_preds.std()
        confidence = max(0.5, min(0.95, 1 / (1 + std)))
    else:
        confidence = 0.75

    return {
        "state": state.strip(),
        "district": district.strip(),
        "season": season.strip(),
        "crop": crop.strip(),
        "area": round(area, 2),
        "predicted_yield": round(pred, 2),
        "confidence": round(confidence, 2),
    }
