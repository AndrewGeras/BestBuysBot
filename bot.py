import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from handlers import handler
from config_data.config import Config, load_config
from storages.storages import storage
from keyboards.main_menu import set_main_menu
from aiogram.fsm.storage.memory import MemoryStorage


# storage = RedisStorage(redis=handler.redis)
# storage = MemoryStorage()

async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
