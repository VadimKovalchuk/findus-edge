import re
import json

from typing import Union

from finvizfinance.quote import finvizfinance as finviz

percent = type('percent', (str,), {'type': float})
FIELD = 'field'
TYPE = 'type'
CORE_DB_MAP = {
    'market_cap': {FIELD: 'Market Cap', TYPE: float},
    'income': {FIELD: 'Income', TYPE: float},
    'sales': {FIELD: 'Sales', TYPE: float},
    'book_share': {FIELD: 'Book/sh', TYPE: float},
    'cash_share': {FIELD: 'Cash/sh', TYPE: float},
    'dividend': {FIELD: 'Dividend', TYPE: float},
    'dividend_percent': {FIELD: 'Dividend %', TYPE: percent},
    'recommendation': {FIELD: 'Recom', TYPE: float},
    'price_earnings': {FIELD: 'P/E', TYPE: float},
    'price_earnings_forward': {FIELD: 'Forward P/E', TYPE: float},
    'price_earnings_growth': {FIELD: 'PEG', TYPE: float},
    'price_sales': {FIELD: 'P/S', TYPE: float},
    'price_book': {FIELD: 'P/B', TYPE: float},
    'price_cash': {FIELD: 'P/C', TYPE: float},
    'price_free_cash': {FIELD: 'P/FCF', TYPE: float},
    'quick_ratio': {FIELD: 'Quick Ratio', TYPE: float},
    'current_ratio': {FIELD: 'Current Ratio', TYPE: float},
    'debt_equity': {FIELD: 'Debt/Eq', TYPE: float},
    'lt_debt_equity': {FIELD: 'LT Debt/Eq', TYPE: float},
    'eps_ttm': {FIELD: 'EPS (ttm)', TYPE: float},
    'eps_next_y': {FIELD: 'EPS next Y', TYPE: percent},
    'eps_next_q': {FIELD: 'EPS next Q', TYPE: float},
    'eps_this_y': {FIELD: 'EPS this Y', TYPE: percent},
    'eps_next_5y': {FIELD: 'EPS next 5Y', TYPE: percent},
    'eps_past_5y': {FIELD: 'EPS past 5Y', TYPE: percent},
    'sales_past_5y': {FIELD: 'Sales past 5Y', TYPE: percent},
    'sales_qq': {FIELD: 'Sales Q/Q', TYPE: percent},
    'eps_qq': {FIELD: 'EPS Q/Q', TYPE: percent},
    'return_asset': {FIELD: 'ROA', TYPE: percent},
    'return_equity': {FIELD: 'ROE', TYPE: percent},
    'return_invest': {FIELD: 'ROI', TYPE: percent},
    'gross_margin': {FIELD: 'Gross Margin', TYPE: percent},
    'oper_margin': {FIELD: 'Oper. Margin', TYPE: percent},
    'profit_margin': {FIELD: 'Profit Margin', TYPE: percent},
    'payout_ratio': {FIELD: 'Payout', TYPE: percent},
    'target_price': {FIELD: 'Target Price', TYPE: float},
    'beta': {FIELD: 'Beta', TYPE: float},
    'sma20': {FIELD: 'SMA20', TYPE: percent},
    'sma50': {FIELD: 'SMA50', TYPE: percent},
    'sma200': {FIELD: 'SMA200', TYPE: percent},
}
FLOAT_PTRN = r'(-)?\d+\.\d+'
MILLION = 'M'
BILLION = 'B'


def convert_value(raw_value: str, target_type: type) -> Union[str, int, float, None]:
    """
    Convert raw value from FinViz response to target type
    :param raw_value: received value
    :param target_type: target conversion type
    :return: converted value
    """
    def float_handler(value: str) -> Union[float, None]:
        result = None
        if ',' in value:
            value = value.replace(',', '')
        match = re.match(FLOAT_PTRN, value)
        if not match:
            return result
        result = match.group(0)
        result = float(result)
        if MILLION in raw_value:
            result = result * 1e6
        if BILLION in raw_value:
            result = result * 1e9
        return result

    def percent_handler(value: str) -> Union[float, None]:
        result = None
        match = re.match(FLOAT_PTRN, value)
        if not match:
            return result
        result = match.group(0)
        result = float(result)
        return result

    type_map = {float: float_handler, percent: percent_handler}
    if raw_value == '-':
        return None
    else:
        return type_map[target_type](raw_value)


def fundamental_raw(arg_dict: dict) -> dict:
    if 'ticker' not in arg_dict:
        raise AttributeError('"ticker" key is missing in arguments dict')
    ticker = arg_dict['ticker']
    tkr = finviz(ticker)
    return tkr.ticker_fundament()


def fundamental(arg_dict: dict) -> str:
    return json.dumps({'values': fundamental_raw(arg_dict)})


def fundamental_converted(arg_dict: dict):
    ticker = arg_dict['ticker']
    result = {}
    values = fundamental_raw(arg_dict)
    converted_values = {}
    for findus_name, params in CORE_DB_MAP.items():
        finviz_name = params[FIELD]
        findus_type = params[TYPE]
        converted_value = convert_value(values[finviz_name], findus_type)
        converted_values[findus_name] = converted_value
        if converted_value is None:
            if 'warnings' not in result:
                result['warnings'] = []
            warn = f'{ticker}: convert {findus_name}({finviz_name}) to None from "{values[finviz_name]}"'
            result['warnings'].append(warn)
    result['values'] = converted_values
    return json.dumps(result)


if __name__ == '__main__':
    # res = fundamental(["MSFT", "O"])
    # print(json.dumps(json.loads(res), indent=4))
    for tkr in ["MSFT", "O", "T"]:
        res = fundamental_converted({'ticker': tkr})
        print(json.dumps(json.loads(res), indent=4))
