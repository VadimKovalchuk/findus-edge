import pandas as pd

LARGE_CAP = ('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 0, 'Symbol')
MID_CAP = ('https://en.wikipedia.org/wiki/List_of_S%26P_400_companies', 0, 'Ticker symbol')
SMALL_CAP = ('https://en.wikipedia.org/wiki/List_of_S%26P_600_companies', 3, 'Ticker symbol')


def getter(link: str, section: int, key: str):
    data = pd.read_html(link)
    table = data[section]
    return table[key].tolist()


def get_sp500_ticker_list():
    return getter(*LARGE_CAP)


def get_sp400_ticker_list():
    return getter(*MID_CAP)


def get_sp600_ticker_list():
    return getter(*SMALL_CAP)


def main():
    for link, section, key in (LARGE_CAP, MID_CAP, SMALL_CAP):
        print(len(getter(link, section, key)))


if __name__ == '__main__':
    main()
