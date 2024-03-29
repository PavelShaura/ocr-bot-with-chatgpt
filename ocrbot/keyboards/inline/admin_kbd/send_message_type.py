from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


send_message_type_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📃  Только текст", callback_data="text_message"),
            InlineKeyboardButton(
                text="🖼  Картинка с текстом", callback_data="image_with_text"
            ),
        ]
    ]
)
