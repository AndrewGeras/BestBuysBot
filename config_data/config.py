from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class DBase:
    db_host: str
    db_name: str
    collection: str


@dataclass
class Config:
    tg_bot: TgBot
    d_base: DBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  d_base=DBase(db_host=env('DB_HOST'),
                               db_name=env('DB_NAME'),
                               collection=env('DB_COLLECTION')))