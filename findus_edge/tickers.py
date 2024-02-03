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
    lst = list(map(lambda x: x.replace('.', '-'), lst))
    return json.dumps(lst)


def get_scope(args: dict):
    scope_name = args.get('scope')
    assert scope_name, 'Scope is not defined'
    scope_params = SCOPES.get(scope_name)
    assert scope_params, f'Unrecognized scope: {scope_name}'
    return getter(*scope_params)


def main():
    for _, scope in SCOPES.items():
        print(getter(*scope))


if __name__ == '__main__':
    main()
