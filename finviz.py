import json

from finvizfinance.quote import finvizfinance as finviz


def fundamental(ticker_list: list):
    result = {}
    for ticker in ticker_list:
        tkr = finviz(ticker)
        fundament = tkr.ticker_fundament()
        result[ticker] = fundament
    return json.dumps(result)


if __name__ == '__main__':
    res = fundamental(["MSFT", "O"])
    print(json.dumps(json.loads(res), indent=4))
