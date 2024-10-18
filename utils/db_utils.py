from config_data.config import Config, load_config
from typing import Any


config: Config = load_config()

client = config.db_client


def get_user_data(uid: int):
    default_data = {
        'items': [],
        'stores': [],
        'matrix': {}
    }
    try:
        database = client[config.db_name]
        collections = database['users']
        user_data = collections.find_one({"_id": uid})  #['user_data']
        if user_data is None:
            collections.insert_one({"_id": uid, 'user_data': default_data})
            client.close()
            return default_data
        client.close()
        return user_data['user_data']

    except Exception as ex:
        print(ex)


def set_user_data(uid: int, user_data: dict[str, Any]):
    try:
        database = client[config.db_name]
        collections = database['users']
        query_filter = {"_id": uid}
        update_data = {'$set': {'user_data': user_data}}
        collections.update_one(query_filter, update_data, upsert=True)
        client.close()

    except Exception as ex:
        print(ex)


#
# user_data = {
#         'items': [],
#         'stores': [],
#         'matrix': {}
#     }
#
# set_user_data(456, user_data)



