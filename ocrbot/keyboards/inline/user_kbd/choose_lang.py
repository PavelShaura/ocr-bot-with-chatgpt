from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choose_lang_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="rus"),
            InlineKeyboardButton(text="Английский", callback_data="eng"),
            InlineKeyboardButton(text="Немецкий", callback_data="gre"),
        ],
        [
            InlineKeyboardButton(text="Китайский упрощенный", callback_data="chs"),
            InlineKeyboardButton(text="Китайский традиционный", callback_data="cht"),
        ],
        [
            InlineKeyboardButton(text="Корейский", callback_data="kor"),
            InlineKeyboardButton(text="Japanese", callback_data="jpn"),
        ],
        [
            InlineKeyboardButton(text="Испансий", callback_data="spa"),
            InlineKeyboardButton(text="Португальский", callback_data="por"),
        ],
        [
            InlineKeyboardButton(text="Итальянский", callback_data="ita"),
            InlineKeyboardButton(text="Французкий", callback_data="fre"),
            InlineKeyboardButton(text="Чешский", callback_data="cze"),
        ],
        [
            InlineKeyboardButton(text="Арабский", callback_data="ara"),
            InlineKeyboardButton(text="Африканский", callback_data="AFR"),
        ],
    ]
)


all_languages = [
    "rus",
    "eng",
    "gre",
    "kor",
    "jpn",
    "chs",
    "cht",
    "spa",
    "por",
    "ita",
    "fre",
    "cze",
    "ara",
    "AFR",
]
