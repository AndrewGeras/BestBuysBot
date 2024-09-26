from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state


from utils import utils
from lexicon import lexicon
from storages.storages import redis




router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    user_name = message.from_user.first_name
    uid = message.from_user.id
    user_data = utils.get_user_data(uid)
    await redis.json().set(str(uid), "$", user_data)

    await message.answer(text=utils.greating(user_name))


@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    uid = message.from_user.id
    data = await redis.json().get(str(uid), "$")
    print(f"data: {data}")
    await message.answer(text=lexicon.LEXICON['help'])


