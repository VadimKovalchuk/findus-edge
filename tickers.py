import pandas as pd


def get_sp500_ticker_list():
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = data[0]
    return table['Symbol'].tolist()
