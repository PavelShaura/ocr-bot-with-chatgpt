import logging
from typing import List, Tuple

from aiogram import Bot

from ocrbot.db.pg_manager import pg_manager


async def get_active_and_blocked_users(
    bot: Bot,
) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
    """
    Получает информацию об активных и заблокированных пользователях.

    :param bot: Объект бота.
    :type bot: aiogram.Bot
    :return: Кортеж, содержащий список всех пользователей, список активных пользователей и список заблокированных пользователей.
    :rtype: tuple[List[Tuple[int, int]], List[int], List[int]]
    """
    active_users: List[int] = []
    blocked_users: List[int] = []
    all_users: List[Tuple[int, int]] = await pg_manager.get_all_users()
    for user_id, chat_id in all_users:
        try:
            chat_member = await bot.get_chat_member(chat_id, user_id)
            chat_member_status = "".join(chat_member.status.split("."))
            if chat_member_status not in ["kicked", "left"]:
                active_users.append(user_id)
            else:
                blocked_users.append(user_id)
        except Exception as e:
            logging.info(
                f"Error when retrieving user information: user_id: {user_id},  exeption: {e}"
            )

    return all_users, active_users, blocked_users
