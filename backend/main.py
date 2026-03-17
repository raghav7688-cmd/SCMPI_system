from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib

from .database import init_db, get_connection
from .crop_recommendation import recommend_crop
from .mandi_analysis import top_markets_for_crop
from .production_analysis import production_vs_demand
from .ai_model import predict_yield

app = FastAPI(title="Smart Crop Planning & Market Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthRequest(BaseModel):
    username: str
    password: str


class RecommendQuery(BaseModel):
    state: str
    season: str


class MandiQuery(BaseModel):
    crop: str


class ProductionQuery(BaseModel):
    state: str


class PredictQuery(BaseModel):
    state: str
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
    except Exception as exc:  # simple uniqueness catch
        raise HTTPException(status_code=400, detail="User already exists") from exc
    return {"message": "registered"}


@app.post("/login")
def login(data: AuthRequest):
    row = get_user(data.username)
    if not row or row["password"] != _hash_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "ok"}


@app.get("/recommend-crop")
def recommend(state: str, season: str):
    result = recommend_crop(state, season)
    if result["recommended_crop"] is None:
        raise HTTPException(status_code=404, detail="No data for selection")
    return result


@app.get("/mandi-prices")
def mandi_prices(crop: str):
    markets = top_markets_for_crop(crop)
    return {"markets": markets}


@app.get("/production-analysis")
def prod_analysis(state: str):
    return production_vs_demand(state)


@app.get("/ai-predict-yield")
def predict(state: str, season: str, crop: str, area: float):
    return predict_yield(state, season, crop, area)

