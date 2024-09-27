from lexicon import lexicon
import json
from typing import Any


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


def save_user_data(uid: int, user_data: dict[str, Any] | list[str], path: str=db_path):
    print('save_user_data')
    with open(path, encoding='utf-8') as db:
        data: dict[str, Any] = json.load(db)

    data[str(uid)] = user_data

    with open(path, 'w', encoding='utf-8') as db:
        json.dump(data, db, indent=4, ensure_ascii=False)

    print(f"данные пользователя сохранены '{uid}' в БД")


def get_item_list(items):
    return "\n".join(
        f"<b><i>{n}. {item}</i></b>" for n, item in enumerate(items, 1)) if items else "<b>Список пока пуст</b>"