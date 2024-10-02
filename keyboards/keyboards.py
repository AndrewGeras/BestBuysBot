from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup,
                           KeyboardButton,ReplyKeyboardMarkup)

from lexicon.lexicon import LEXICON_BTN as btns, LEXICON_COMMANDS as cmds, LEXICON

# 'cancel' button
cancel_btn = KeyboardButton(text=btns['cancel'])
cancel_kb = ReplyKeyboardMarkup(keyboard=[[cancel_btn]], resize_keyboard=True)


# 'stop' button
stop_btn = KeyboardButton(text=btns['stop'])
stop_kb = ReplyKeyboardMarkup(keyboard=[[stop_btn]], resize_keyboard=True)


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
del_item_btn = InlineKeyboardButton(
    text=btns['del_item'],
    callback_data='del_item'
)
fin_edit_btn = InlineKeyboardButton(
    text=btns['stop'],
    callback_data='stop'
)
edit_item_list_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[[add_item_btn, del_item_btn], [fin_edit_btn]]
)


def create_list_kb_markup(item_type: str) -> InlineKeyboardMarkup:
    item = LEXICON[item_type]
    add_btn = InlineKeyboardButton(
        text = f'{btns['add_item']} {item}',
        callback_data='add_item'
    )
    del_btn = InlineKeyboardButton(
        text=f'{btns['del_item']} {item}',
        callback_data='del_item'
    )
    fin_btn = InlineKeyboardButton(
        text=btns['stop'],
        callback_data='stop'
    )
    return InlineKeyboardMarkup(inline_keyboard=[[add_btn, del_btn], [fin_btn]])


def create_list_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    """create list of items or stores as inline keyboard"""
    if isinstance(items, list):
        inline = [[InlineKeyboardButton(text=item, callback_data=item)] for item in items]
    if isinstance(items, dict):
        inline = [[InlineKeyboardButton(text=f"{item} >> {price if price else 'н/д'}",
                                        callback_data=item)]
                  for item, price in items.items()]
    inline.append([InlineKeyboardButton(text=btns['cancel'], callback_data='cancel')])
    return InlineKeyboardMarkup(inline_keyboard=inline)
