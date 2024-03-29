from aiogram.filters import BaseFilter
from aiogram.types import Message

from ocrbot.config import config


class AdminFilter(BaseFilter):
    """
    Фильтр для определения, является ли пользователь администратором бота.
    """

    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        """
        Проверяет, является ли пользователь администратором бота.

        :param obj: Объект сообщения.
        :type obj: aiogram.types.Message
        :return: True, если пользователь является администратором, в противном случае False.
        :rtype: bool
        """
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin
