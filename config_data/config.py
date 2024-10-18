from dataclasses import dataclass
from pymongo import MongoClient
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db_client: MongoClient
    db_name: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  db_client=MongoClient(host=env('DB_HOST')),
                  db_name=env('DB_NAME'))