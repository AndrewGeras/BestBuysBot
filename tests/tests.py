from utils import utils
import json
import os


test_db_path = 'test_db.json'

def test_get_user_data(uid: str, items: str|None=None, stores: str|None=None):

    with open(test_db_path, encoding='utf-8') as db:
        data: dict = json.load(db)

        if items is not None:
            data[uid]['items'].append(items)
        if stores is not None:
            data[uid]['stores'].append(stores)

        user_data = data.get(uid)

    if items is not None or stores is not None:
        with open(test_db_path, 'w', encoding='utf-8') as db:
            json.dump(data, db, indent=4, ensure_ascii=False)

    return user_data



# тест на добавление нового пользователя в БД
uid = '123'
user_data = utils.get_user_data(uid, path=test_db_path)
test_user_data = test_get_user_data(uid)
assert user_data == test_user_data

# тест на добавление ещё одного нового пользователя в БД
uid = '456'
user_data = utils.get_user_data(uid, path=test_db_path)
test_user_data = test_get_user_data(uid)
assert user_data == test_user_data

# тест на проверку сохранения данных существующего пользователя в БД
uid = '123'
test_user_data = test_get_user_data(uid, items='apple', stores='lidl')
user_data = utils.get_user_data(uid, path=test_db_path)
assert user_data == test_user_data