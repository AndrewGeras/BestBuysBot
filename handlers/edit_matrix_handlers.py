from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from typing import Any

from lexicon.lexicon import LEXICON_BTN, LEXICON
from states.states import FSMEditMatrix as FSMstate
from keyboards import keyboards
from utils import utils


"""These handlers process everything about store-item matrix"""

router = Router()


@router.callback_query(StateFilter(FSMstate.wait_for_store_chs), F.data == 'cancel')
async def process_cancel_store_chs(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    user_data = await state.get_data()
    utils.save_user_data(uid, user_data)
    await callback.message.delete()
    await state.clear()


@router.callback_query(StateFilter(FSMstate.wait_for_item_chs), F.data == 'cancel')
async def process_cancel_item_chs(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_data.pop('temp_store', None)
    await callback.message.edit_text(
        text=LEXICON['chs_store'],
        reply_markup=keyboards.create_list_keyboard(user_data['stores'])
    )
    await state.set_data(user_data)
    await state.set_state(FSMstate.wait_for_store_chs)


@router.callback_query(StateFilter(FSMstate.wait_for_store_chs))
async def process_chs_store(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    store = callback.data
    await callback.message.edit_text(
        text=LEXICON['chs_item'],
        reply_markup=keyboards.create_list_keyboard(user_data['matrix'][store])
    )
    await state.update_data(data={'temp_store': store})
    await state.set_state(FSMstate.wait_for_item_chs)


@router.callback_query(StateFilter(FSMstate.wait_for_item_chs))
async def process_chs_item(callback: CallbackQuery, state: FSMContext):
    item = callback.data.split(f" {LEXICON['div']} ")[0]
    await callback.message.edit_text(text=LEXICON['send_price'])
    await state.update_data(data={'temp_item': item})
    await state.set_state(FSMstate.wait_for_price_input)


@router.message(StateFilter(FSMstate.wait_for_price_input), F.text.regexp(r'^\d*$|^\d+\.\d+$|^\d+,\d+$'))
async def process_price_input(message: Message, state: FSMContext):
    price = message.text.replace(',', '.')
    user_data = await state.get_data()
    item = user_data.pop('temp_item')
    store = user_data['temp_store']
    user_data['matrix'][store][item] = round(float(price), 2)
    await message.answer(
        text=LEXICON['chs_item'],
        reply_markup=keyboards.create_list_keyboard(user_data['matrix'][store])
    )
    await state.set_data(user_data)
    await state.set_state(FSMstate.wait_for_item_chs)


@router.message(StateFilter(FSMstate.wait_for_price_input))
async def process_nondigit_price(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['non_digit'])


@router.message(StateFilter(FSMstate.wait_for_store_chs,
                            FSMstate.wait_for_item_chs))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()