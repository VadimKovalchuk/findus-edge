import json

import yfinance

from pandas import DataFrame

START_DATE = '2023-01-01'


def ticker_history(arg_dict: dict):
    if 'ticker' not in arg_dict:
        raise AttributeError('"ticker" key is missing in arguments dict')
    tkr = yfinance.Ticker(arg_dict['ticker'])
    if 'start' not in arg_dict:
        arg_dict['start'] = START_DATE
    history = tkr.history(start=arg_dict['start'])
    history.reset_index(inplace=True)
    history['Date'] = history['Date'].apply(lambda x: x.isoformat()[:10])
    result = {
        'prices': [],
        'dividends': [],
        'splits': []
    }
    for indx in range(history.shape[0]):
        row = history.loc[indx]
        result['prices'].append((row['Date'],
                                 round(row['Open'], 2),
                                 round(row['High'], 2),
                                 round(row['Low'], 2),
                                 round(row['Close'], 2),
                                 float(row['Volume'])))
        if row['Dividends']:
            result['dividends'].append((row['Date'], row['Dividends']))
        if row['Stock Splits']:
            result['splits'].append((row['Date'], row['Stock Splits']))
    return json.dumps(result)


if __name__ == '__main__':
    res = ticker_history({"ticker": "MSFT", "start": "2022-05-10"})
    #print(res)
    print(json.dumps(json.loads(res), indent=4))
    #tkr = yfinance.Ticker("MSFT")
    #print(json.dumps(tkr.get_info(), indent=4))

