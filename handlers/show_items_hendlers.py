from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from states.states import FSMShowItems as FSMstate
from keyboards.keyboards import create_list_keyboard, chs_show_mtd_kb_markup
from utils import utils


"""These handlers process display results"""

router = Router()


@router.callback_query(StateFilter(FSMstate.wait_for_method_chs), F.data == 'cancel')
async def process_cancel_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()


@router.callback_query(StateFilter(FSMstate.wait_for_store_chs), F.data == 'cancel')
async def process_cancel_str_chs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f"<b>{LEXICON['show_method']}</b>",
        reply_markup=chs_show_mtd_kb_markup
    )
    await state.set_state(FSMstate.wait_for_method_chs)


@router.callback_query(StateFilter(FSMstate.wait_for_method_chs), F.data == 'show_list')
async def process_show_list_callback(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.edit_text(text=f'<b>{LEXICON['list_best_price']}</b> '
                                          f'{utils.get_list_stores(user_data)}')
    await state.clear()


@router.callback_query(StateFilter(FSMstate.wait_for_method_chs), F.data == 'chs_store')
async def process_chs_store_mthd_callback(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.edit_text(
        text=LEXICON['chs_store'],
        reply_markup=create_list_keyboard(user_data['stores'], key='stores')
    )
    await state.set_state(FSMstate.wait_for_store_chs)


@router.callback_query(StateFilter(FSMstate.wait_for_store_chs))
async def process_store_chs_callback(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    store = callback.data
    await callback.message.edit_text(
        text=f'В магазине <b>{store}</b> {LEXICON['list_best_in_store']}'
             f'{utils.get_best_in_store(user_data, store)}'
    )
    await state.clear()


@router.message(StateFilter(FSMstate.wait_for_method_chs,
                            FSMstate.wait_for_store_chs))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()