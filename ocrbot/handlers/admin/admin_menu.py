import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ocrbot.filters.is_admin import AdminFilter
from ocrbot.keyboards.reply.admin_kbd.admin_menu import admin_menu_keyboard

admin_menu_router: Router = Router()


@admin_menu_router.message(
    Command("admin"), AdminFilter(), flags={"throttling_key": "default"}
)
async def is_admin_menu(message: Message) -> None:
    """
    Обработчик команды /admin для администратора.

    Отображает меню администратора с возможностью просмотра активных и заблокированных пользователей,
    а также осуществления рассылки всем пользователям.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    """
    name: str = message.from_user.full_name
    await message.answer(
        text=f"Приветствую тебя, <b>{name} </b>👋\n\n"
        f"<b>Это меню администратора</b> 🔐\n\n"
        f"<i>Здесь Вы можете посмотреть активных и заблокированных пользователей, а так же сделать рассылку всем пользователям.</i>",
        reply_markup=admin_menu_keyboard,
        parse_mode="HTML",
    )
    logging.info(f"{name} logged in as administrator.")
