import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram import Bot

from ocrbot.filters.is_admin import AdminFilter
from ocrbot.services.check_user_status import get_active_and_blocked_users

get_len_users_router: Router = Router()


@get_len_users_router.message(
    F.text == "Колличество пользователей 👨‍👩‍👧‍👦",
    AdminFilter(),
    flags={"throttling_key": "default"},
)
async def is_admin_menu(message: Message, bot: Bot) -> None:
    """
    Обработчик команды для получения информации о количестве пользователей.

    Отображает количество всех пользователей бота, активных пользователей и заблокированных пользователей.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    :param bot: Объект бота.
    :type bot: aiogram.Bot
    """
    name: str = message.from_user.full_name
    all_users, active_users, blocked_users = await get_active_and_blocked_users(bot)
    await message.answer(
        text=f"В боте всего <code>{len(all_users)}</code> пользователей\n\n  *********************  \n"
        f"✅   Активные: <code>{len(active_users)}</code>\n  *********************  \n"
        f"🚫  Заблокированные: <code>{len(blocked_users)}</code>\n  *********************  \n ",
        parse_mode="HTML",
    )
    logging.info(f"Received list of users by administrator {name}")
