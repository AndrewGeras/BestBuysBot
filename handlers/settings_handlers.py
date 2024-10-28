from ctypes import string_at

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from typing import Any

from lexicon.lexicon import LEXICON_BTN, LEXICON, LEXICON_COMMANDS
from states.states import FSMSettings as FSMstate
from keyboards import keyboards
from utils import utils, db_utils


"""These handlers process everything about settings"""


router = Router()


@router.message(StateFilter(FSMstate.wait_for_send_of_curr), F.text == LEXICON_BTN['stop'])
async def process_stop_input_curr_marker(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=LEXICON['settings'],
        reply_markup=keyboards.create_list_keyboard(user_data['settings'], key='settings')
    )
    await state.set_state(FSMstate.wait_for_setting_chs)
    await message.delete()


@router.callback_query(StateFilter(FSMstate.wait_for_setting_chs), F.data == 'cancel')
async def process_of_finish_settings(callback: CallbackQuery, state: FSMContext, db_conf_data):
    uid = callback.from_user.id
    user_data = await state.get_data()
    db_utils.save_user_data(uid, user_data, db_conf_data)
    await state.clear()
    await callback.message.delete()


@router.callback_query(StateFilter(FSMstate.wait_for_setting_chs), F.data == 'currency')
async def process_choice_of_setting(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['send_currency'])
    await state.set_state(FSMstate.wait_for_send_of_curr)


@router.message(StateFilter(FSMstate.wait_for_send_of_curr), F.text & ~F.text.in_(LEXICON_COMMANDS))
async def process_input_of_curr_marker(message: Message, state: FSMContext):
    text = message.text
    if len(text) > 5:
        await message.answer(text=LEXICON['long_curr'])
    elif set(text).intersection('0123456789'):
        await message.answer(text=LEXICON['no_digits'])
    else:
        user_data = await state.get_data()
        settings = user_data['settings']
        settings.update({'currency': text})
        await state.update_data(data={'settings': settings})
        await message.answer(
            text=LEXICON['settings'],
            reply_markup=keyboards.create_list_keyboard(user_data['settings'], key='settings')
        )
        await state.set_state(FSMstate.wait_for_setting_chs)


@router.message(StateFilter(FSMstate.wait_for_setting_chs,
                            FSMstate.wait_for_send_of_curr))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()