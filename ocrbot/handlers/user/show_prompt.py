from aiogram import Router, F
from aiogram.types import CallbackQuery

from ocrbot.db.pg_manager import pg_manager
from ocrbot.keyboards.inline.user_kbd.action_after_image_loading import (
    action_after_loading_keyboard,
)

show_text_router: Router = Router()


@show_text_router.callback_query(
    F.data == "show_prompt", flags={"throttling_key": "callback"}
)
async def show_text(query: CallbackQuery) -> None:
    """
    Показывает последний сохраненный текст пользователю.

    :param query: Колбэк-запрос.
    :type query: aiogram.types.CallbackQuery
    """
    user_id = query.from_user.id
    prompt_text = await pg_manager.get_latest_prompt_by_user_id(user_id)
    if prompt_text:
        await query.message.answer(
            text=prompt_text, reply_markup=action_after_loading_keyboard
        )
    else:
        await query.message.edit_text(text="Текст не найден")
