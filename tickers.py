import pandas as pd

LARGE_CAP = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

def get_sp500_ticker_list():
    data = pd.read_html(LARGE_CAP)
    table = data[0]
    return table['Symbol'].tolist()
