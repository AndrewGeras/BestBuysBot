from typing import Any
from itertools import chain

from lexicon.lexicon import LEXICON


def greating(user_name: str) -> str:
    """returns the new user greeting"""

    return (f'Привет {user_name}!👋🏻'
            f'\n{LEXICON["start"]}')


def update_items(user_data: dict[str, Any]) -> dict[str, Any]:
    """Makes <items> collections in <matrix> equal to <items> collection in <user_data>.
       Returns updated <user_data>."""


    items = user_data['items']
    matrix = user_data['matrix']

    if not matrix:
        return user_data

    m_items = tuple(matrix.values())[0].keys()

    if set(items) == set(m_items):
        return user_data

    miss_items = set(items).difference(m_items)
    ext_items = set(m_items).difference(items)

    for store in matrix:
        [matrix[store].pop(key) for key in ext_items]
        matrix[store].update(dict().fromkeys(miss_items, None))

    user_data['matrix'] = matrix
    return user_data


def update_stores(user_data: dict[str, Any]) -> dict[str, Any]:
    """Makes <stores> collections in <matrix> equal to <store> collection in <user_data>.
           Returns updated <user_data>."""

    items = user_data['items']
    stores = user_data['stores']
    matrix = user_data['matrix']
    m_stores = matrix.keys()

    if set(stores) == set(m_stores):
        return user_data

    miss_stores = set(stores).difference(m_stores)
    ext_stores = set(m_stores).difference(stores)

    [matrix.pop(store) for store in ext_stores]
    matrix.update(dict().fromkeys(miss_stores, dict().fromkeys(items, None)))

    user_data['matrix'] = matrix
    return user_data


def change_user_data(user_data: dict[str, Any], old: str, new: str, key: str) -> dict[str, Any] | None:
    """Changes old item or store to new one in user_data's matrix
            Returns updated <user_data>."""

    collection = user_data[key]
    matrix: dict = user_data['matrix']

    if new in collection:
        return None
    user_data[key] = [item if item != old else new for item in collection]

    user_data.pop('temp', None)

    if key == 'stores':
        if not matrix or matrix.get(old) is None:
            return user_data
        matrix[new] = matrix.pop(old, None)

    elif key == 'items':
        if not matrix or old not in tuple(matrix.values())[0]:
            return user_data
        for store in matrix:
            matrix[store][new] = matrix[store].pop(old, None)

    user_data['matrix'] = matrix
    return user_data


def get_item_list(items):
    """Returns list of items or stores"""

    return "\n".join(f"{n}. {item}" for n, item in enumerate(sorted(items), 1)) if items else "⚠️ список пуст"


def is_empty_prices(matrix):
    """Return True if all prices are None"""

    return not any(chain.from_iterable(_.values() for _ in matrix.values()))


def get_best_price(user_data: dict[str, Any]) -> list[dict[str, Any]]:
    """gathers info about best price for items in stores"""

    items = user_data['items']
    matrix = user_data['matrix']

    best_price = {item: min((i[item] for i in matrix.values() if i[item] is not None), default=None) for item in items}

    return [{
        'name': item,
        'store': tuple(filter(lambda x: matrix[x][item] == best_price[item], matrix)),
        'price': best_price[item]
    } for item in best_price]


def get_list_stores(user_data: dict[str, Any]) -> str:
    """Returns items list as string with names of stores where price is the best"""

    list_stores = get_best_price(user_data)
    currency = user_data['settings']['currency']
    if currency is None:
        currency = LEXICON['def_curr']

    return "\n\n".join(f'{n}. <u>{item["name"]}</u>\n\t\t\t\t'
                       f'лучшая цена <b>{item["price"]} {currency}</b>'
                       f' в магазин{("е", "ах")[len(item["store"]) > 1]} <b>{", ".join(item["store"])}</b>'
                       if item["price"] is not None
                       else f'{n}. <u>{item["name"]}:</u>\n\t\t\t\t'
                            f'{LEXICON["empty_data"]}'
                       for n, item in enumerate(sorted(list_stores, key=lambda x: x['name']), 1))


def get_best_in_store(user_data: dict[str, Any], store: str) -> str:
    """Returns items list as string with price in a specific store if its price is the best"""

    currency = user_data['settings']['currency']
    if currency is None:
        currency = LEXICON['def_curr']

    if all(price is None for price in user_data['matrix'][store].values()):
        return LEXICON['empty_prices_in_store']

    list_items = [item for item in get_best_price(user_data)
                  if store in tuple(item['store'])
                  and item["price"] is not None]
    if list_items:
        return '\n\n'.join(f'{n}. <u>{item["name"]}</u>\n\t\t\t\tцена: <b>{item["price"]} {currency}</b>'
                           for n, item in enumerate(sorted(list_items, key=lambda x: x['name']), 1))
    return LEXICON['all_expensive']