from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


show_text_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📌  Показать текст запроса", callback_data="show_prompt"
            )
        ]
    ]
)
