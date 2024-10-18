from config_data.config import Config, load_config
from pymongo import MongoClient
from typing import Any


config: Config = load_config()


def get_user_data(uid: int):
    default_data = {
        'items': [],
        'stores': [],
        'matrix': {}
    }
    client = MongoClient(host=config.d_base.host)
    try:
        database = client[config.d_base.db_name]
        collections = database[config.d_base.collection]
        user_data = collections.find_one({"_id": uid})
        if user_data is None:
            collections.insert_one({"_id": uid, 'user_data': default_data})
            client.close()
            return default_data
        client.close()
        return user_data['user_data']

    except Exception as ex:
        print(ex)


def save_user_data(uid: int, user_data: dict[str, Any]):

    client = MongoClient(host=config.d_base.host)

    try:
        database = client[config.d_base.db_name]
        collections = database[config.d_base.collection]
        query_filter = {"_id": uid}
        update_data = {'$set': {'user_data': user_data}}
        collections.update_one(query_filter, update_data, upsert=True)
        client.close()

    except Exception as ex:
        print(ex)
