import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from ocrbot.db.pg_manager import pg_manager
from ocrbot.gpt4free.completion import try_models
from ocrbot.keyboards.inline.user_kbd.show_text import show_text_keyboard

shipping_to_gpt_router: Router = Router()


@shipping_to_gpt_router.callback_query(
    F.data.in_(["go_to_chat", "send_again"]),
    flags={"throttling_key": "callback"},
)
async def shipping_text_to_chat_gpt(query: CallbackQuery) -> None:
    """
    Отправляет текст на обработку в модель ИИ и выводит ответ.

    :param query: Колбэк-запрос.
    :type query: aiogram.types.CallbackQuery
    """
    user_id = query.from_user.id
    prompt_text = await pg_manager.get_latest_prompt_by_user_id(user_id)

    if prompt_text:
        text = f"🔅 ОТВЕТ 🔅\n\n"
        try:
            await query.message.edit_text(text="Печатает . . . ")
            response = await try_models(prompt_text)
            text += response
            await query.message.edit_text(text=text, reply_markup=show_text_keyboard)
        except Exception as e:
            await query.message.answer(
                text="Произошла ошибка во время запроса",
                reply_markup=show_text_keyboard,
            )
            logging.info(f"All models failed to generate a response: {e}")
    else:
        await query.message.edit_text(text="Текст не найден")
