from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

import pyupbit
from prophet import Prophet


origins = [
    '*',
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/tickers')
async def tickers():
    tickers = pyupbit.get_tickers()
    krw_tickers = [ticker for ticker in tickers if 'KRW' in ticker]
    return krw_tickers


@app.get('/tickers/{ticker}/data')
async def get_data(ticker):
    data = pyupbit.get_ohlcv(ticker=ticker, count=180)
    data['ds'] = data.index.tz_localize(None)
    data['y'] = data.close
    forecast = predict(data[['ds', 'y']])
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    result = pd.merge(forecast, data[['ds', 'y']], on='ds', how='outer')
    result = result.fillna('')
    # print(result.columns)
    return result.values.T.tolist()


def predict(df):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    return forecast
