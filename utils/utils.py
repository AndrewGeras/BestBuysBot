from lexicon import lexicon
import json
from typing import Any

from lexicon.lexicon import LEXICON

db_path = 'db.json'

def greating(user_name: str) -> str:
    return f'Привет {user_name}! {lexicon.LEXICON["start"]}'


def get_user_data(uid: int, path: str=db_path) -> dict:

    default_data = {
        'items': [],
        'stores': [],
        'matrix': {}
    }

    with open(path, encoding='utf-8') as db:
        data: dict = json.load(db)

    user_data = data.get(str(uid))
    if user_data is None:
        user_data = default_data
        data.setdefault(uid, user_data)

        with open(path, 'w', encoding='utf-8') as db:
            json.dump(data, db, indent=4, ensure_ascii=False)


    return user_data


def update_items(user_data: dict[str, Any]) -> dict[str, Any]:
    items = user_data['items']
    matrix = user_data['matrix']
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


def save_user_data(uid: int, user_data: dict[str, Any] | list[str], path: str=db_path):
    # print('save_user_data')
    with open(path, encoding='utf-8') as db:
        data: dict[str, Any] = json.load(db)

    data[str(uid)] = user_data

    with open(path, 'w', encoding='utf-8') as db:
        json.dump(data, db, indent=4, ensure_ascii=False)

    # print(f"данные пользователя сохранены '{uid}' в БД")


def get_item_list(items):
    return "\n".join(
        f"<b><i>{n}. {item}</i></b>" for n, item in enumerate(items, 1)) if items else "<b>Список пока пуст</b>"


def get_default_matrix(user_data: dict):
    items = user_data['items']
    stores = user_data['stores']
    return {store: {item: None for item in items} for store in stores}


