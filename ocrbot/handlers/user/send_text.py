import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from ocrbot.config import redis_client
from ocrbot.db.pg_manager import pg_manager
from ocrbot.keyboards.inline.user_kbd.action_after_image_loading import (
    action_after_loading_keyboard,
)
from ocrbot.services.extracting_text import extract_text
from ocrbot.keyboards.inline.user_kbd.choose_lang import all_languages

send_text_router: Router = Router()


@send_text_router.callback_query(
    F.data.in_(all_languages), flags={"throttling_key": "callback"}
)
async def handle_callback(query: CallbackQuery) -> None:
    """
    Обработчик колбэк-запроса для извлечения текста на выбранном языке.

    :param query: Колбэк-запрос.
    :type query: aiogram.types.CallbackQuery
    """
    user_id = query.from_user.id
    language = query.data
    file_path = await redis_client.get_file_path(user_id)
    if file_path:
        await query.message.edit_text(
            "✂️  Извлечение текста, пожалуйста, подождите . . ."
        )
        try:
            extracted_text = await extract_text(file_path, language)
        except Exception as e:
            await query.message.edit_text(
                text=f"<i>Не удалось извлеч текст с картинки. \n"
                "Возможно картинка плохого качества, или на ней нет текста . . .</i>",
                parse_mode="HTML",
            )
            logging.info(f"Failed to extract text from image. Error: {e}")
        else:
            msg = await query.message.edit_text(
                text=f"🔸  ВАШ ТЕКСТ 🔸\n\n{extracted_text}",
                reply_markup=action_after_loading_keyboard,
            )
            chat_id = msg.chat.id
            await pg_manager.save_query(user_id, extracted_text, chat_id)
    else:
        await query.message.edit_text(
            text="<i>Что-то пошло не так, отправьте это изображение еще раз . . .</i>",
            parse_mode="HTML",
        )
        logging.info(f"Something went wrong when a user {user_id} submitted an image")
