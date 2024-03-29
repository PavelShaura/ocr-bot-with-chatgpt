from aioredis import Redis


class AsyncRedisClient(Redis):
    """
    Асинхронный клиент для работы с Redis.
    """

    def __init__(self, redis_instance: Redis, *args, **kwargs) -> None:
        """
        Инициализация асинхронного клиента Redis.

        :param redis_instance: Экземпляр клиента Redis.
        :type redis_instance: aioredis.Redis
        """
        super().__init__(*args, **kwargs)
        self.redis = redis_instance

    async def set_file_path(self, user_id: str, file_path: str) -> None:
        """
        Устанавливает путь к файлу в Redis для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :param file_path: Путь к файлу.
        :type file_path: str
        """
        await self.redis.set(f"photo:{user_id}", file_path)

    async def get_file_path(self, user_id: str) -> str:
        """
        Получает путь к файлу из Redis для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Путь к файлу или None, если файл не найден.
        :rtype: str
        """
        file_path = await self.redis.get(f"photo:{user_id}")
        return file_path if file_path else None
