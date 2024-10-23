from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from typing import Any

from lexicon.lexicon import LEXICON_BTN, LEXICON
from states.states import FSMEditItemsList as FSMstate
from keyboards import keyboards
from utils import utils, db_utils


"""These handlers process everything about item list"""

router = Router()


@router.message(StateFilter(FSMstate.input_item), F.text == LEXICON_BTN['stop'])
async def process_stop_adding(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"{LEXICON['chg_items']}\n\n{utils.get_item_list(user_data['items'])}",
        reply_markup=keyboards.create_list_kb_markup('item'))
    await state.set_state(FSMstate.waiting_for_choice)
    await message.delete()


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('stop', 'no')))
async def process_cancel_callback(callback: CallbackQuery, state: FSMContext, db_conf_data):
    uid = callback.from_user.id
    user_data = await state.get_data()
    user_data = utils.update_items(user_data)
    db_utils.save_user_data(uid, user_data, db_conf_data)
    await state.clear()
    await callback.message.delete()


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('add_item', 'yes')))
async def process_choose_add_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['send_item'])
    await state.set_state(FSMstate.input_item)


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data == 'del_item')
async def process_choose_del_item(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item_list = user_data['items']
    if item_list:
        await callback.message.edit_text(text=LEXICON['choice_item'],
                                         reply_markup=keyboards.create_list_keyboard(item_list))
        await state.set_state(FSMstate.delete_item)
    else:
        await callback.message.edit_text(text=LEXICON['empty_list'],
                                         reply_markup=keyboards.yes_no_kb_markup)
        await state.set_state(FSMstate.waiting_for_choice)


@router.message(StateFilter(FSMstate.input_item), F.text)
async def process_input_item(message: Message, state: FSMContext):
    user_data: dict[str, Any] = await state.get_data()
    items = user_data['items']
    item = message.text[:30]
    if item in items:
        await message.answer(text=f'<b>{item}</b> {LEXICON["in_list"]}',
                             reply_markup=keyboards.stop_kb)
    else:
        items.append(item)
        await message.answer(text=f'<b>{item}</b> {LEXICON["got_it"]}',
                             reply_markup=keyboards.stop_kb)
        user_data['items'] = items
        await state.update_data(user_data)


@router.callback_query(StateFilter(FSMstate.delete_item), F.data == 'cancel')
async def process_cancel_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await state.set_state(FSMstate.waiting_for_choice)
    await callback.message.edit_text(
        text=f"{LEXICON['chg_items']}\n\n{utils.get_item_list(user_data['items'])}",
        reply_markup=keyboards.create_list_kb_markup('item'))


@router.callback_query(StateFilter(FSMstate.delete_item))
async def process_item_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item = callback.data
    user_data['items'].remove(item)
    await state.set_data(user_data)
    await callback.message.edit_text(text=f'<b>{item}</b> {LEXICON["cross_out"]}\n\n'
                                          f"{LEXICON['chg_items']}\n\n{utils.get_item_list(user_data['items'])}",
                                     reply_markup=keyboards.create_list_kb_markup('item'))
    await state.set_state(FSMstate.waiting_for_choice)


@router.message(StateFilter(FSMstate.delete_item, FSMstate.waiting_for_choice))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()