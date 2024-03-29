from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить картинку 🖼"),
        ],
        [
            KeyboardButton(text="Спросить у ChatGPT 💬"),
        ],
    ],
    resize_keyboard=True,
)
