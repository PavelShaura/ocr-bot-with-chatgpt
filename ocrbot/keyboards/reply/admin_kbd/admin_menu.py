from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Колличество пользователей 👨‍👩‍👧‍👦"),
            KeyboardButton(text="Сделать расылку 💬"),
        ],
    ],
    resize_keyboard=True,
)
