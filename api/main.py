from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


from prophet import Prophet
import pyupbit


TICKERS = pyupbit.get_tickers()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/tickers')
async def get_tickers():
    global TICKERS
    return [ticker for ticker in TICKERS if ticker.startswith('KRW')]


@app.get('/tickers/{ticker}')
async def get_prices(ticker):
    df = pyupbit.get_ohlcv(ticker, count=365*3)
    df = df[['close']].copy()
    df.columns = ['y']
    df['ds'] = df.index
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    print(forecast.columns)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    print(result.head())
    return {
        # 'ds': result['ds'].astype('str').values.tolist()
        'result': result.values.T.tolist()
    }


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
