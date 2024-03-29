from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


send_own_text_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔍  Отправить в ChatGPT", callback_data="go_to_chat"
            )
        ]
    ]
)
