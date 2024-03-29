from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.types import Message

from ocrbot.config import redis_client, config
from ocrbot.keyboards.inline.user_kbd.choose_lang import choose_lang_keyboard

get_photo_router: Router = Router()


@get_photo_router.message(
    F.text == "Отправить картинку 🖼", flags={"throttling_key": "default"}
)
async def handle_photo(message: Message) -> None:
    """
    Обработчик команды для отправки изображения.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    """
    await message.answer(text="⏳  Загрузите картинку в чат . . .")


@get_photo_router.message(
    F.content_type == ContentType.PHOTO, flags={"throttling_key": "default"}
)
async def handle_photo(message: Message, bot: Bot) -> None:
    """
    Обработчик получения изображения.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    :param bot: Объект бота.
    :type bot: aiogram.Bot
    """
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = (
        f"https://api.telegram.org/file/bot{config.tg_bot.token}/{file.file_path}"
    )
    user_id = message.from_user.id
    await redis_client.set_file_path(user_id, file_path)
    await message.answer(
        "На каком языке текст с картинки?", reply_markup=choose_lang_keyboard
    )
