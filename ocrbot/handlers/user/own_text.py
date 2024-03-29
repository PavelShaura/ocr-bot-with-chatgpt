from typing import Union

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ocrbot.db.pg_manager import pg_manager
from ocrbot.keyboards.inline.user_kbd.send_own_text import send_own_text_keyboard
from ocrbot.states.states import FSMFillForm

own_text_router: Router = Router()


@own_text_router.callback_query(
    F.data.in_(["own_text"]),
    flags={"throttling_key": "callback"},
)
@own_text_router.message(
    F.text == "Спросить у ChatGPT 💬", flags={"throttling_key": "default"}
)
async def own_text(query: Union[Message, CallbackQuery], state: FSMContext) -> None:
    """
    Обработчик запроса на отправку собственного текста.

    :param query: Объект сообщения или запроса обратного вызова.
    :type query: Union[aiogram.types.Message, aiogram.types.CallbackQuery]
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    message: Message = query if isinstance(query, Message) else query.message
    msg = await message.answer(text="📎  Отправьте свой текст в чат . . .")
    chat_id = msg.chat.id
    await state.set_state(FSMFillForm.rewritten_prompt)
    await state.update_data(chat_id=chat_id)


@own_text_router.message(StateFilter(FSMFillForm.rewritten_prompt))
async def process_rewritten_prompt(message: Message, state: FSMContext) -> None:
    """
    Обработчик получения собственного текста.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    data = await state.get_data()
    chat_id = data.get("chat_id")
    user_id = message.from_user.id
    prompt_text = message.text
    await pg_manager.save_query(user_id, prompt_text, chat_id)
    await message.answer(
        text=f"📎  Ваш текст:\n\n{prompt_text}", reply_markup=send_own_text_keyboard
    )
    await state.clear()
