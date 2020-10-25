import datetime as dt
import pandas as pd
import pandas_datareader.data as web

START_DATE = dt.date(2015, 1, 1)
TODAY = dt.date.today()


def get_ticker_prices(ticker: str,
                      provider: str = 'yahoo',
                      start: dt.date = START_DATE,
                      end: dt.date = TODAY):
    df = web.DataReader(ticker, provider, start, end)
    return df


print(get_ticker_prices('O'))
