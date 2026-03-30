from fastapi import FastAPI
import pandas as pd
import joblib
from pydantic import BaseModel
from typing import List

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# LOAD DATA (FIX MULTIINDEX SAFELY)
# -------------------------------
df = pd.read_csv("stock_data.csv")

# Clean column names (important fix)
df.columns = df.columns.str.strip()

# If MultiIndex somehow exists, flatten it safely
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [col[0] for col in df.columns]

# Convert Date to string (for JSON)
if 'Date' in df.columns:
    df['Date'] = df['Date'].astype(str)


# -------------------------------
# LOAD MODEL
# -------------------------------
model = joblib.load("model.pkl")


# -------------------------------
# PYDANTIC MODELS
# -------------------------------

class StockData(BaseModel):
    Date: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float


class Summary(BaseModel):
    high: float
    low: float
    average: float


class CompareResponse(BaseModel):
    symbol1: str
    symbol2: str
    message: str


# -------------------------------
# ROOT (OPTIONAL)
# -------------------------------
@app.get("/")
def home():
    return {"message": "Stock API is running"}


# -------------------------------
# 1. COMPANIES
# -------------------------------
@app.get("/companies", response_model=List[str])
def get_companies():
    return ["INFY", "TCS"]


# -------------------------------
# 2. LAST 30 DAYS DATA
# -------------------------------
@app.get("/data/{symbol}", response_model=List[StockData])
def get_data(symbol: str):
    data = df.tail(30)
    return data.to_dict(orient="records")


# -------------------------------
# 3. SUMMARY (FIXED)
# -------------------------------
@app.get("/summary/{symbol}", response_model=Summary)
def get_summary(symbol: str):
    df_clean = df.dropna()

    return {
        "high": float(df_clean['Close'].max()),
        "low": float(df_clean['Close'].min()),
        "average": float(df_clean['Close'].mean())
    }


# -------------------------------
# 4. COMPARE
# -------------------------------
import yfinance as yf

@app.get("/compare")
def compare(symbol1: str, symbol2: str):

    df1 = yf.download(symbol1 + ".NS", period="1mo")
    df2 = yf.download(symbol2 + ".NS", period="1mo")

    avg1 = df1['Close'].mean()
    avg2 = df2['Close'].mean()

    return {
        "symbol1": symbol1,
        "symbol2": symbol2,
        "avg_price_symbol1": float(avg1),
        "avg_price_symbol2": float(avg2),
        "message": "Comparison using real data"
    }