import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ocrbot.keyboards.reply.user_kbd.menu import menu_keyboard

command_start_router: Router = Router()


@command_start_router.message(CommandStart(), flags={"throttling_key": "default"})
async def user_start(message: Message) -> None:
    """
    Обрабатывает команду старта от пользователя и отправляет приветственное сообщение с меню.

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :return: None
    """
    user_id: int = message.from_user.id
    name: str = message.from_user.full_name
    photo_url: str = (
        "https://www.aiseesoft.com/images/tutorial/picture-to-text/picture-to-text.jpg"
    )
    await message.answer_photo(
        photo=photo_url,
        caption=f"Приветствую Вас,  {name}! 👋\n\n"
        f"Я умею извлекать текст из изображения "
        f"и отправлять его в ChatGPT. \n"
        f"Это значит, что вы можете забить на скучное переписывание вопросов "
        f"и сэкономить кучу времени на экзамене! 🥳\n\n"
        f"-- <i>Нельзя копировать текст во время теста?</i> \n"
        f"-- 🚫 <i>Не вопрос!</i> ⏬\n\n"
        f"<b>1. Просто сделайте скрин и отправьте его мне. 📸 \n"
        f"2. Я прочту всё, что там написано, и дам вам ответ! 🤖\n\n</b>"
        f"💪 Удачи на экзамене! 😎🔥\n\n"
        f"<i>По всем вопросам писать администратору: </i> https://t.me/PavelShau",
        reply_markup=menu_keyboard,
        parse_mode="HTML",
    )
    logging.info(f"User:{name}, ID:{user_id} came to see us!")
