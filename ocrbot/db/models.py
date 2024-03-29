from ocrbot.db.database import db
from datetime import datetime


class UserData(db.Model):
    """
    Модель запроса к базе данных PostgreSQL.
    """

    __tablename__ = "user_data"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.BigInteger)
    timestamp: datetime = db.Column(db.DateTime)
    chat_id: int = db.Column(db.BigInteger)
    prompt_text: str = db.Column(db.String)

    def __init__(
        self,
        user_id: int,
        timestamp: datetime,
        chat_id: int,
        prompt_text: str,
        **kwargs
    ) -> None:

        super().__init__(**kwargs)
        self.__values__.update(kwargs)
        self.user_id = user_id
        self.timestamp = timestamp
        self.chat_id = chat_id
        self.prompt_text = prompt_text
