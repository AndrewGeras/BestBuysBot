from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from typing import Any

from keyboards.keyboards import cancel_kb
from lexicon.lexicon import LEXICON_BTN
from states.states import FSMEditItemsList as FSMstate
from lexicon import lexicon
from keyboards import keyboards
from utils import utils

router = Router()


@router.message(StateFilter(FSMstate.input_item, FSMstate.delete_item), F.text == LEXICON_BTN['cancel'])
async def process_cancel_press(message: Message, state: FSMContext):
    uid = message.from_user.id
    user_data = await state.get_data()
    utils.save_user_data(uid, user_data)
    await state.clear()


# # this handler processes choose
# @router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('cancel', 'no')))
# async def process_choose_cancel(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_text(text='Вы вернулись в стартовый режим')
#     await state.clear()


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data == 'cancel')
async def process_cancel_callback(callback: CallbackQuery, state: FSMContext):
    print('process_cancel_callback')
    uid = callback.from_user.id
    user_data = await state.get_data()
    print(user_data)
    utils.save_user_data(uid, user_data)
    await state.clear()
    await callback.message.delete()


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data.in_(('add_item', 'yes')))
async def process_choose_add_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=f'Отправь мне интересующие тебя товары, каждый в отдельном сообщении.')
    await state.set_state(FSMstate.input_item)


@router.callback_query(StateFilter(FSMstate.waiting_for_choice), F.data == 'del_item')
async def process_choose_del_item(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item_list = user_data['items']
    if item_list:
        await callback.message.edit_text(text=f"Выбери товар, который необходимо удалить:",
                                         reply_markup=keyboards.create_list_keyboard(item_list))
        await state.set_state(FSMstate.delete_item)
    else:
        await callback.message.edit_text(text=f"Список товаров сейчас пуст, добавим что-нибудь?",
                                         reply_markup=keyboards.yes_no_kb_markup)



@router.message(StateFilter(FSMstate.input_item), F.text)
async def process_input_item(message: Message, state: FSMContext):
    user_data: dict[str, Any] = await state.get_data()
    item = message.text[:30]
    user_data['items'].append(item)
    await message.answer(text=f'<b>{item}</b> записал',
                         reply_markup=cancel_kb)
    await state.update_data(user_data)
    data = await state.get_data()
    # print(data)


@router.callback_query(StateFilter(FSMstate.delete_item))
async def process_item_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    item = callback.data
    user_data['items'].remove(item)
    await state.set_data(user_data)
    await callback.message.edit_text(text=f'<b>{item}</b> удалил',
                                     reply_markup=keyboards.edit_item_list_kb_markup)
    await state.set_state(FSMstate.waiting_for_choice)



