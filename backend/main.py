from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import hashlib
from pathlib import Path

from .ai_model import predict_yield
from .crop_recommendation import recommend_crop
from .database import get_connection, init_db
from .mandi_analysis import get_crop_price_estimate
from .production_analysis import production_vs_demand

app = FastAPI(title="Smart Crop Planning & Market Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class AuthRequest(BaseModel):
    username: str
    password: str


class RecommendQuery(BaseModel):
    state: str
    district: str
    season: str


class MandiQuery(BaseModel):
    state: str
    district: str
    season: str


class ProductionQuery(BaseModel):
    state: str


class PredictQuery(BaseModel):
    state: str
    district: str
    season: str
    crop: str
    area: float


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    return cur.fetchone()


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Backend is running. See /docs for interactive API docs.",
    }


@app.get("/favicon.ico")
def favicon():
    return {"status": "ok"}


@app.post("/register")
def register(data: AuthRequest):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data.username, _hash_password(data.password)),
        )
        conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="User already exists") from exc
    return {"message": "registered"}


@app.post("/login")
def login(data: AuthRequest):
    row = get_user(data.username)
    if not row or row["password"] != _hash_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "ok"}


@app.get("/recommend-crop")
def recommend(state: str, district: str, season: str):
    result = recommend_crop(state, district, season)
    if result["crop"] is None:
        raise HTTPException(status_code=404, detail="No data for selection")
    return result


@app.get("/mandi-prices")
def mandi_prices(state: str, district: str, season: str):
    recommendation = recommend_crop(state, district, season)
    if recommendation["crop"] is None:
        raise HTTPException(status_code=404, detail="No district-level crop found for market estimation")

    price_estimate = get_crop_price_estimate(recommendation["crop"], district)
    return {
        "state": state.strip(),
        "district": district.strip(),
        "season": season.strip(),
        "crop": recommendation["crop"],
        "estimated_price": price_estimate["estimated_price"],
        "latest_price_column": price_estimate["latest_price_column"],
        "label": price_estimate["label"],
    }


@app.get("/production-analysis")
def prod_analysis(state: str):
    return production_vs_demand(state)


@app.get("/ai-predict-yield")
def predict(state: str, district: str, season: str, crop: str, area: float):
    return predict_yield(state, district, season, crop, area)
