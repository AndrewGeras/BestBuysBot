from aiogram.fsm.storage.redis import Redis, RedisStorage


redis = Redis(decode_responses=True)
storage = RedisStorage(redis=redis)