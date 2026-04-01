from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import webbrowser
import yfinance as yf
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/companies")
def get_companies():
    return [
        "INFY","TCS","RELIANCE","HCLTECH","WIPRO",
        "SBIN","ICICIBANK","HDFCBANK","AXISBANK",
        "ITC","LT","BHARTIARTL","KOTAKBANK"
    ]

@app.get("/data/{symbol}")
def get_data(symbol: str, days: int = 30):
    try:
        df = yf.download(symbol + ".NS", period="3mo")

        if df is None or df.empty:
            return []

        df = df.reset_index().tail(days)

        result = []
        for _, row in df.iterrows():
            result.append({
                "date": str(row["Date"]),
                "close": float(row["Close"])
            })

        return result

    except Exception as e:
        return {"error": str(e)}

@app.get("/stats/{symbol}")
def get_stats(symbol: str):
    try:
        df = yf.download(symbol + ".NS", period="1y")

        if df is None or df.empty:
            return {"error": "No data"}

        df = df.reset_index()
        df["daily_return"] = (df["Close"] - df["Open"]) / df["Open"]

        return {
            "symbol": symbol.upper(),
            "52_week_high": float(df["High"].max()),
            "52_week_low": float(df["Low"].min()),
            "average_close": float(df["Close"].mean()),
            "latest_close": float(df["Close"].iloc[-1]),
            "latest_daily_return": round(float(df["daily_return"].iloc[-1]) * 100, 2)
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
