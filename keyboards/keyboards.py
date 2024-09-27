from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup,
                           KeyboardButton,ReplyKeyboardMarkup)

from lexicon.lexicon import LEXICON_BTN as btns


# 'cancel' button
cancel_btn = KeyboardButton(text=btns['cancel'])
cancel_kb = ReplyKeyboardMarkup(keyboard=[[cancel_btn]], resize_keyboard=True)


#create 'yes/no' keyboard
yes_btn = InlineKeyboardButton(
    text=btns['yes'],
    callback_data='yes'
)
no_btn = InlineKeyboardButton(
    text=btns['no'],
    callback_data='no'
)
yes_no_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[[yes_btn, no_btn]]
)


# create 'edit item list' keyboard
add_item_btn = InlineKeyboardButton(
    text=btns['add_item'],
    callback_data='add_item'
)
show_item_list = InlineKeyboardButton(
    text=btns['show_list'],
    callback_data='show_list'
)
del_item_btn = InlineKeyboardButton(
    text=btns['del_item'],
    callback_data='del_item'
)
fin_edit_btn = InlineKeyboardButton(
    text=btns['cancel'],
    callback_data='cancel'
)

edit_item_list_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[[add_item_btn, del_item_btn], [fin_edit_btn]]
)

def create_list_keyboard(items: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=item,
                                               callback_data=item)] for item in items]
    )
