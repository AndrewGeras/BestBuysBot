from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON_COMMANDS, LEXICON_BTN, LEXICON
from utils import utils, db_utils
from lexicon import lexicon
from states.states import FSMEditItemsList, FSMEditStoreList, FSMEditMatrix, FSMShowItems, FSMSettings
from keyboards.keyboards import create_list_kb_markup, create_list_keyboard, chs_show_mtd_kb_markup

from typing import Any


"""These handlers process main menu commands"""


router = Router()


@router.message(Command(commands='az5'))
async def process_hard_reset_command(message: Message, state: FSMContext):
    """this temp handler is for hard-reset"""
    await message.answer(text="бот в исходном состоянии")
    await state.clear()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """this handler processes 'start'-command"""
    user_name = message.from_user.first_name
    uid = message.from_user.id
    await message.answer(text=utils.greating(user_name))


@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    """this handler processes 'help'-command"""
    await message.answer(text=lexicon.LEXICON['help'])


@router.message(Command(commands='item_list'), StateFilter(default_state))
async def process_eil_command(message: Message, state: FSMContext, db_conf_data):
    """this handler processes 'edit item list'-command"""
    uid = message.from_user.id
    user_data = db_utils.get_user_data(uid, db_conf_data)
    await state.set_data(user_data)

    await message.answer(
        text=f"<b>{LEXICON['chg_items']}</b>\n\n{utils.get_item_list(user_data['items'])}",
        reply_markup=create_list_kb_markup('item'))
    await state.set_state(FSMEditItemsList.waiting_for_choice)


@router.message(Command(commands='store_list'), StateFilter(default_state))
async def process_esl_command(message: Message, state: FSMContext, db_conf_data):
    """this handler processes 'edit store list'-command"""
    uid = message.from_user.id
    user_data: dict[str, Any] = db_utils.get_user_data(uid, db_conf_data)

    await state.set_data(user_data)
    await message.answer(
        text=f"<b>{LEXICON['chg_stores']}</b>\n\n{utils.get_item_list(user_data['stores'])}",
        reply_markup=create_list_kb_markup('store'))
    await state.set_state(FSMEditStoreList.waiting_for_choice)


@router.message(Command(commands='price_table'), StateFilter(default_state))
async def process_edit_mtrx_command(message: Message, state: FSMContext, db_conf_data):
    """This handler processes 'edit matrix'-command"""
    uid = message.from_user.id
    user_data: dict[str, Any] = db_utils.get_user_data(uid, db_conf_data)
    if not user_data['items']:
        await message.answer(text=LEXICON['fill_item_list'])
    elif not user_data['stores']:
        await message.answer(text=LEXICON['fill_store_list'])
    else:
        await message.answer(
            text=LEXICON['chs_store'],
            reply_markup=create_list_keyboard(user_data['stores'], key='stores')
        )
        await state.set_state(FSMEditMatrix.wait_for_store_chs)
        await state.set_data(user_data)


@router.message(Command(commands='shopping_list'), StateFilter(default_state))
async def process_show_store_command(message: Message, state: FSMContext, db_conf_data):
    """This handler processes 'show_store' command"""
    uid = message.from_user.id
    user_data: dict[str, Any] = db_utils.get_user_data(uid, db_conf_data)
    if not user_data['matrix']:
        await message.answer(text=LEXICON['empty_matrix'])
    elif utils.is_empty_prices(user_data['matrix']):
        await message.answer(text=LEXICON['empty_prices'])
    else:
        await message.answer(
            text=LEXICON['show_method'],
            reply_markup=chs_show_mtd_kb_markup
        )
        await state.set_state(FSMShowItems.wait_for_method_chs)
        await state.set_data(user_data)


@router.message(Command(commands='settings'), StateFilter(default_state))
async def process_settings_command(message: Message, state: FSMContext, db_conf_data):
    """This handler processes 'settings' command"""
    uid = message.from_user.id
    user_data = db_utils.get_user_data(uid, db_conf_data)
    await message.answer(
        text=LEXICON['settings'],
        reply_markup=create_list_keyboard(user_data['settings'], key='settings')
    )
    await state.set_state(FSMSettings.wait_for_setting_chs)
    await state.set_data(user_data)


@router.message(StateFilter(default_state), ~F.text_in_(LEXICON_COMMANDS))
async def process_idler_update(message: Message):
    """this handler processes any not command update sent in default state"""
    await message.delete()
