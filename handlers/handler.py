from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import Redis

from asyncio import Lock

from utils import utils
from lexicon import lexicon


redis = Redis(host='localhost', decode_responses=True)
router = Router()
lock = Lock()

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    user_name = message.from_user.first_name
    uid = message.from_user.id
    async with lock:
        user_data = await utils.get_user_data(uid)
        redis.set(uid, user_data)
    await message.answer(text=utils.greating(user_name))


@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=lexicon.LEXICON['help'])