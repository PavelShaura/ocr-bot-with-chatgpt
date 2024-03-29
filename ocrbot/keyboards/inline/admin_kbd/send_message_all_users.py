from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


send_message_all_users_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝  Отправить ВСЕМ", callback_data="send_all"),
            InlineKeyboardButton(
                text="❌  Отмена ", callback_data="cancel_send_message"
            ),
        ]
    ]
)
