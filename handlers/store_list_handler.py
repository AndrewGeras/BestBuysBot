from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from typing import Any
from pprint import pprint

from lexicon.lexicon import LEXICON_BTN, LEXICON
from states.states import FSMEditStoreList as FSMstate
from keyboards import keyboards
from utils import utils, db_utils


"""These handlers process everything about store list"""

router = Router()


@router.message(StateFilter(FSMstate.add_store), F.text == LEXICON_BTN['stop'])
async def process_stop_adding(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"{LEXICON['chg_stores']}\n\n{utils.get_item_list(user_data['stores'])}",
        reply_markup=keyboards.create_list_kb_markup('store'))
    await state.set_state(FSMstate.waiting_for_choice)
    await message.delete()


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('stop', 'no')))
async def process_cancel_callback(callback: CallbackQuery, state: FSMContext, db_conf_data):
    uid = callback.from_user.id
    user_data = await state.get_data()
    user_data = utils.update_stores(user_data)
    db_utils.save_user_data(uid, user_data, db_conf_data)
    await state.clear()
    await callback.message.delete()


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('add_item', 'yes')))
async def process_choose_add_store(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['send_store'])
    await state.set_state(FSMstate.add_store)


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('edit_item', 'del_item')))
async def process_choose_edit_or_del_store(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item_list = user_data['stores']
    action = callback.data
    if item_list:
        await callback.message.edit_text(text=LEXICON[action],
                                         reply_markup=keyboards.create_list_keyboard(item_list))
        if action == 'edit_item':
            await state.set_state(FSMstate.edit_store)
        elif action == 'del_item':
            await state.set_state(FSMstate.delete_store)
    else:
        await callback.message.edit_text(text=LEXICON['empty_list'],
                                         reply_markup=keyboards.yes_no_kb_markup)
        await state.set_state(FSMstate.waiting_for_choice)


@router.message(StateFilter(FSMstate.add_store), F.text)
async def process_input_store(message: Message, state: FSMContext):
    user_data: dict[str, Any] = await state.get_data()
    stores: list = user_data['stores']
    store = message.text[:30]
    if store in stores:
        await message.answer(text=f'<b>{store}</b> {LEXICON["in_list"]}',
                             reply_markup=keyboards.stop_kb)
    else:
        stores.append(store)
        user_data['stores'] = stores
        await state.update_data(user_data)
        await message.answer(text=f'<b>{store}</b> {LEXICON["got_it"]}',
                             reply_markup=keyboards.stop_kb)


@router.message(StateFilter(FSMstate.change_store), F.text)
async def process_change_store(message: Message, state: FSMContext):
    user_data: dict[str, Any] = await state.get_data()
    store = message.text[:30]
    old_store = user_data.get('temp')

    changed_data = utils.change_user_data(user_data, old_store, store, 'stores')

    if changed_data is None:
        await message.answer(text=f'<b>{store}</b> {LEXICON["in_list"]}',
                             reply_markup=keyboards.stop_kb)
    else:
        await state.set_data(changed_data)
        await message.answer(
            text=f"{LEXICON['chg_stores']}\n\n{utils.get_item_list(changed_data['stores'])}",
            reply_markup=keyboards.create_list_kb_markup('store'))
        await state.set_state(FSMstate.waiting_for_choice)


@router.callback_query(StateFilter(FSMstate.delete_store, FSMstate.edit_store), F.data == 'cancel')
async def process_cancel_edit_or_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await state.set_state(FSMstate.waiting_for_choice)
    await callback.message.edit_text(
        text=f"{LEXICON['chg_stores']}\n\n{utils.get_item_list(user_data['stores'])}",
        reply_markup=keyboards.create_list_kb_markup('store'))


@router.callback_query(StateFilter(FSMstate.edit_store))
async def process_edit_store(callback: CallbackQuery, state: FSMContext):
    store = callback.data
    await state.update_data(data={'temp': store})
    await callback.message.edit_text(text=f'{LEXICON["send_new_store"]} <b>{store}</b>')
    await state.set_state(FSMstate.change_store)


@router.callback_query(StateFilter(FSMstate.delete_store))
async def process_store_delete(callback: CallbackQuery, state: FSMContext):
    store = callback.data
    await state.update_data(data={'temp': store})
    await callback.message.edit_text(text=f'{LEXICON['del_store_confirm']} <b>{store}</b>?',
                                     reply_markup=keyboards.yes_no_kb_markup)
    await state.set_state(FSMstate.delete_confirm)


@router.callback_query(StateFilter(FSMstate.delete_confirm), F.data == 'no')
async def process_reject_delete_store(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item_list = user_data['stores']
    user_data.pop('temp', None)
    await state.set_data(user_data)
    await callback.message.edit_text(text=LEXICON['del_item'],
                                     reply_markup=keyboards.create_list_keyboard(item_list))
    await state.set_state(FSMstate.delete_store)


@router.callback_query(StateFilter(FSMstate.delete_confirm), F.data == 'yes')
async def process_confirm_delete_store(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    store = user_data.pop('temp', None)
    if store:
        user_data['stores'].remove(store)
    await callback.message.edit_text(text=f'<b>{store}</b> {LEXICON["cross_out"]}\n\n'
                                          f"{LEXICON['chg_stores']}\n\n{utils.get_item_list(user_data['stores'])}",
                                     reply_markup=keyboards.create_list_kb_markup('store'))
    await state.set_data(user_data)
    await state.set_state(FSMstate.waiting_for_choice)


@router.message(StateFilter(FSMstate.delete_store,
                            FSMstate.edit_store,
                            FSMstate.waiting_for_choice,
                            FSMstate.delete_confirm))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()