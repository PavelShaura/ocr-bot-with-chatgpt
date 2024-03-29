from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


action_after_loading_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔍  Отправить в ChatGPT", callback_data="go_to_chat"
            )
        ],
        [InlineKeyboardButton(text="✏️  Написать свой текст", callback_data="own_text")],
    ]
)
