from config_data.config import Config, load_config
from pymongo import MongoClient
from typing import Any


# config: Config = load_config()


def get_user_data(uid: int, conf_data: dict[str, str]):
    default_data = {
        'items': [],
        'stores': [],
        'matrix': {}
    }
    client = MongoClient(host=conf_data['db_host'])

    try:
        database = client[conf_data['db_name']]
        collection = database[conf_data['collection']]
        user_data = collection.find_one({"_id": uid})
        if user_data is None:
            collection.insert_one({"_id": uid, 'user_data': default_data})
            client.close()
            return default_data
        client.close()
        return user_data['user_data']

    except Exception as ex:
        print(ex)


def save_user_data(uid: int, user_data: dict[str, Any], conf_data: dict[str, str]):

    client = MongoClient(host=conf_data['db_host'])

    try:
        database = client[conf_data['db_name']]
        collection = database[conf_data['collection']]
        query_filter = {"_id": uid}
        update_data = {'$set': {'user_data': user_data}}
        collection.update_one(query_filter, update_data, upsert=True)
        client.close()

    except Exception as ex:
        print(ex)
