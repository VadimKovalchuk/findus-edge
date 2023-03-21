import json

import pandas as pd

SCOPES = {
    'SP500': ('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 0, 'Symbol'),
    'SP400': ('https://en.wikipedia.org/wiki/List_of_S%26P_400_companies', 0, 'Symbol'),
    'SP600': ('https://en.wikipedia.org/wiki/List_of_S%26P_600_companies', 0, 'Symbol')
}


def getter(link: str, section: int, key: str):
    data = pd.read_html(link)
    table = data[section]
    lst = table[key].to_list()
    return json.dumps(lst)


def get_scope(args: dict):
    scope = args.get('scope')
    assert scope, 'Scope is not defined'
    return getter(*scope)


def main():
    for _, scope in SCOPES.items():
        print(getter(*scope))


if __name__ == '__main__':
    main()
