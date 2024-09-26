from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON_COMMANDS, LEXICON_BTN
from utils import utils
from lexicon import lexicon
from storages.storages import redis
from states.states import FSMEditItemsList, FSMEditStoreList
from keyboards.keyboards import cancel_kb

from typing import Any


"""Here are collected main menu commands handlers"""

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """this handler processes 'start'-command"""
    user_name = message.from_user.first_name
    uid = message.from_user.id
    utils.get_user_data(uid)
    # await redis.json().set(str(uid), "$", user_data)
    await message.answer(text=utils.greating(user_name))


@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    """this handler processes 'help'-command"""
    # uid = message.from_user.id
    # user_data = await state.get_data()
    # data = await redis.json().get(str(uid), "$")
    # print(f"data: {user_data}")
    await message.answer(text=lexicon.LEXICON['help'])


@router.message(Command(commands='edit_item_list'), StateFilter(default_state))
async def process_eil_command(message: Message, state: FSMContext):
    """this handler processes 'edit item list'-command"""
    uid = message.from_user.id
    user_data: dict[str, Any] = utils.get_user_data(uid)

    # user_data = await redis.json().get(str(uid), "$")
    # if user_data is None:
    #     user_data = utils.get_user_data(uid)

    await state.set_data(user_data)

    await message.answer(
        text="Выбери действие",
        reply_markup=cancel_kb)
    await state.set_state(FSMEditItemsList.waiting_for_choice)


@router.message(Command(commands='edit_store_list'), StateFilter(default_state))
async def process_esl_command(message: Message, state: FSMContext):
    """this handler processes 'edit store list'-command"""
    uid = message.from_user.id
    user_data: dict[str, Any] = utils.get_user_data(uid)

    await state.set_data(user_data)
    await message.answer(
        text="Выбери действие",
        reply_markup=cancel_kb)
    await state.set_state(FSMEditStoreList.waiting_for_choice)


@router.message(F.text == LEXICON_BTN['cancel'])
async def procces_cancel_btn_press(message: Message, state: FSMContext):
    """this handler processes pressing cancel-button during any none default state"""
    await message.answer(text='Вы вернулись в стартовый режим')
    await state.clear()
    await message.delete()


@router.message(StateFilter(default_state), ~F.text_in_(LEXICON_COMMANDS))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()

