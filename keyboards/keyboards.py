from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup,
                           KeyboardButton,ReplyKeyboardMarkup)

from lexicon.lexicon import LEXICON_BTN


# 'cancel' button
cancel_btn =KeyboardButton(text=LEXICON_BTN['cancel'])
cancel_kb =ReplyKeyboardMarkup(keyboard=[[cancel_btn]],resize_keyboard=True)