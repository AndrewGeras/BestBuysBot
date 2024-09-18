import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config_data.config import Config, load_config


async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()


if __name__ == '__main__':
    asyncio.run(main())
