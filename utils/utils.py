from lexicon import lexicon
import json
import os


db_path = os.path.join('..', 'db.json')

def greating(user_name: str) -> str:
    return f'Привет {user_name}! {lexicon.LEXICON["start"]}'


def get_user_data(uid: str, path: str = db_path) -> dict:
    default_data = {
        'items': [],
        'stores': [],
        'matrix': {}
    }

    with open(path, encoding='utf-8') as db:
        data: dict = json.load(db)

    user_data = data.get(uid)
    if user_data is None:
        user_data = default_data
        data.setdefault(uid, user_data)

        with open(path, 'w', encoding='utf-8') as db:
            json.dump(data, db, indent=4, ensure_ascii=False)

    return user_data