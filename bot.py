import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_data.config import Config, load_config

from handlers import mmc_handlers, item_list_handlers, store_list_handler, edit_matrix_handlers, show_items_hendlers
from storages.storages import storage
from keyboards.main_menu import set_main_menu


async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(mmc_handlers.router)
    dp.include_router(item_list_handlers.router)
    dp.include_router(store_list_handler.router)
    dp.include_router(edit_matrix_handlers.router)
    dp.include_router(show_items_hendlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
