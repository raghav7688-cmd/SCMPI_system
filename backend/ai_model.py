import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from pathlib import Path

from .dataset_loader import load_crop_data

MODEL_PATH = Path(__file__).parent / "model.joblib"


def build_pipeline(df: pd.DataFrame) -> Pipeline:
    features = ["State_Name", "Season", "Crop", "Area", "Crop_Year"]
    X = df[features]
    y = df["Production"]

    categorical = ["State_Name", "Season", "Crop"]
    numeric = ["Area", "Crop_Year"]

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
    df = load_crop_data()
    pipe = build_pipeline(df)
    X = df[["State_Name", "Season", "Crop", "Area", "Crop_Year"]]
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
    return joblib.load(MODEL_PATH)


def predict_yield(state: str, season: str, crop: str, area: float) -> dict:
    model = load_model()
    df = pd.DataFrame(
        [{"State_Name": state, "Season": season, "Crop": crop, "Area": area, "Crop_Year": 2025}]
    )
    pred = float(model.predict(df)[0])
    # crude confidence proxy using tree variance
    if hasattr(model.named_steps["model"], "estimators_"):
        est_preds = np.vstack([tree.predict(model.named_steps["preprocess"].transform(df)) for tree in model.named_steps["model"].estimators_])
        std = est_preds.std()
        confidence = max(0.5, min(0.95, 1 / (1 + std)))
    else:
        confidence = 0.75
    return {"predicted_yield": round(pred, 2), "confidence": round(confidence, 2)}

