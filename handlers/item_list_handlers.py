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


@router.message(StateFilter(FSMstate.add_item), F.text == LEXICON_BTN['stop'])
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
    await state.set_state(FSMstate.add_item)


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('edit_item', 'del_item')))
async def process_choose_edit_or_del_item(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item_list = user_data['items']
    action = callback.data
    if item_list:
        await callback.message.edit_text(text=LEXICON[action],
                                         reply_markup=keyboards.create_list_keyboard(item_list))
        if action == 'edit_item':
            await state.set_state(FSMstate.edit_item)
        elif action == 'del_item':
            await state.set_state(FSMstate.delete_item)
    else:
        await callback.message.edit_text(text=LEXICON['empty_list'],
                                         reply_markup=keyboards.yes_no_kb_markup)
        await state.set_state(FSMstate.waiting_for_choice)


@router.message(StateFilter(FSMstate.add_item), F.text)
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


@router.message(StateFilter(FSMstate.change_item), F.text)
async def process_change_item(message: Message, state: FSMContext):
    user_data: dict[str, Any] = await state.get_data()
    item = message.text[:30]
    old_item = user_data.get('temp')

    changed_data = utils.change_user_data(user_data, old_item, item, 'items')

    if changed_data is None:
        await message.answer(text=f'<b>{item}</b> {LEXICON["in_list"]}',
                             reply_markup=keyboards.stop_kb)
    else:
        await state.set_data(changed_data)
        await message.answer(
            text=f"{LEXICON['chg_items']}\n\n{utils.get_item_list(changed_data['items'])}",
            reply_markup=keyboards.create_list_kb_markup('item'))
        await state.set_state(FSMstate.waiting_for_choice)


@router.callback_query(StateFilter(FSMstate.edit_item, FSMstate.delete_item), F.data == 'cancel')
async def process_cancel_edit_of_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await state.set_state(FSMstate.waiting_for_choice)
    await callback.message.edit_text(
        text=f"{LEXICON['chg_items']}\n\n{utils.get_item_list(user_data['items'])}",
        reply_markup=keyboards.create_list_kb_markup('item'))


@router.callback_query(StateFilter(FSMstate.edit_item))
async def process_edit_item(callback: CallbackQuery, state: FSMContext):
    item = callback.data
    await state.update_data(data={'temp': item})
    await callback.message.edit_text(text=f'{LEXICON["send_new_item"]} <b>{item}</b>')
    await state.set_state(FSMstate.change_item)


@router.callback_query(StateFilter(FSMstate.delete_item))
async def process_item_delete(callback: CallbackQuery, state: FSMContext):
    item = callback.data
    await state.update_data(data={'temp_item': item})
    await callback.message.edit_text(text=f'{LEXICON['del_item_confirm']} <b>{item}</b>?',
                                     reply_markup=keyboards.yes_no_kb_markup)
    await state.set_state(FSMstate.delete_confirm)


@router.callback_query(StateFilter(FSMstate.delete_confirm), F.data == 'no')
async def process_reject_delete_item(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item_list = user_data['items']
    user_data.pop('temp_item', None)
    await state.set_data(user_data)
    await callback.message.edit_text(text=LEXICON['del_item'],
                                     reply_markup=keyboards.create_list_keyboard(item_list))
    await state.set_state(FSMstate.delete_item)


@router.callback_query(StateFilter(FSMstate.delete_confirm), F.data == 'yes')
async def process_confirm_delete_item(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item = user_data.pop('temp_item', None)
    if item:
        user_data['items'].remove(item)
    await callback.message.edit_text(text=f'<b>{item}</b> {LEXICON["cross_out"]}\n\n'
                                          f"{LEXICON['chg_stores']}\n\n{utils.get_item_list(user_data['items'])}",
                                     reply_markup=keyboards.create_list_kb_markup('item'))
    await state.set_data(user_data)
    await state.set_state(FSMstate.waiting_for_choice)


@router.message(StateFilter(FSMstate.delete_item,
                            FSMstate.waiting_for_choice,
                            FSMstate.delete_confirm))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()