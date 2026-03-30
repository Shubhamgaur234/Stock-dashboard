# Stock Data Intelligence Dashboard

## Overview

This project is a simple stock data platform built as part of an internship assignment.
I worked with stock market data, created some useful features, and built APIs to serve the data.

---

## What I Did

* Collected stock data using yfinance
* Cleaned and processed it with Pandas
* Created features like moving average, lag values, and volatility
* Built a Linear Regression model to predict next day price
* Created APIs using FastAPI
* Used Pydantic for data validation

---

## Model

The model predicts the next day's closing price.
It performs well on test data (R² ~0.95) and captures the overall trend, though it slightly lags on sudden changes.

---

## API Endpoints

* `/companies`
* `/data/{symbol}`
* `/summary/{symbol}`
* `/compare`

Swagger docs:
http://127.0.0.1:8000/docs

---

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Tech Stack

Python, FastAPI, Pandas, Scikit-learn, yfinance

---

## Note

This project helped me understand data processing, feature engineering, and building APIs with real data.
