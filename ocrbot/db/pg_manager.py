from datetime import datetime
from sqlalchemy import select, distinct
from ocrbot.db.models import UserData
from ocrbot.db.database import db as db_instance
from typing import Optional, List, Tuple


class QueryManager:
    """
    Менеджер запросов в БД PostgreSQL.
    """

    def __init__(self, db) -> None:
        """
        Инициализация менеджера запросов.

        :param db: Экземпляр базы данных.
        :type db: gino.Gino
        """
        self.db = db

    async def save_query(
        self,
        user_id: int,
        prompt_text: str,
        chat_id: int,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Сохраняет запрос пользователя в базе данных.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :param prompt_text: Текст запроса.
        :type prompt_text: str
        :param chat_id: Идентификатор чата пользователя.
        :type chat_id: int
        :param timestamp: Временная метка запроса (по умолчанию None).
        :type timestamp: Optional[datetime]
        """
        if timestamp is None:
            timestamp = datetime.now()
        await UserData.create(
            user_id=user_id,
            timestamp=timestamp,
            chat_id=chat_id,
            prompt_text=prompt_text,
        )

    async def get_latest_prompt_by_user_id(self, user_id: int) -> Optional[str]:
        """
        Получает последний запрос пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Текст последнего запроса пользователя или None, если запросов нет.
        :rtype: Optional[str]
        """
        query = (
            select(UserData)
            .where(UserData.user_id == user_id)
            .order_by(UserData.timestamp.desc())
            .limit(1)
        )
        latest_query = await self.db.first(query)
        if latest_query:
            return latest_query.prompt_text
        else:
            return None

    async def get_all_users(self) -> List[Tuple[int, int]]:
        """
        Получить всех уникальных пользователей с их chat_id и user_id.

        :return: Список кортежей (user_id, chat_id).
        :rtype: List[Tuple[int, int]]
        """
        query = select([distinct(UserData.user_id), UserData.chat_id])
        all_users = await self.db.all(query)
        return all_users


pg_manager = QueryManager(db_instance)
