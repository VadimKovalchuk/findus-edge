import json
from typing import Union

import yfinance

from pandas import DataFrame

START_DATE = '2016-01-01'

def pd_to_dict(dataframe: DataFrame):
    pass


def get_ticker_data(parameters: dict):
                    # ticker: str,
                    # method_name: str,
                    # arguments: dict = {},
                    # post_method_name: str = ''):
    tkr = yfinance.Ticker(parameters['ticker'])
    attribute = getattr(tkr, parameters['method_name'])
    if isinstance(attribute, type(tkr.get_calendar)):
        result = attribute()
    else:
        result = attribute
    if parameters.get('post_method_name'):
        post_method = getattr(result, parameters['post_method_name'])
        return post_method()
    else:
        return result


def ticker_history(ticker: str, start: str = START_DATE):
    tkr = yfinance.Ticker(ticker)
    history = tkr.history(start=start)
    history.reset_index(inplace=True)
    history['Date'] = history['Date'].apply(lambda x: x.isoformat()[:10])
    result = {
        'prices': [],
        'dividends': [],
        'splits': []
    }
    for indx in range(history.shape[0]):
        row = history.loc[indx]
        result['prices'].append((row['Date'], row['Close']))
        if row['Dividends']:
            result['dividends'].append((row['Date'], row['Dividends']))
        if row['Stock Splits']:
            result['splits'].append((row['Date'], row['Stock Splits']))
    return result


if __name__ == '__main__':
    res = ticker_history("MSFT")
    print(json.dumps(res))

