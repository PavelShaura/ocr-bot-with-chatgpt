import logging
from typing import Union

from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ocrbot.filters.is_admin import AdminFilter
from ocrbot.keyboards.inline.admin_kbd.send_message_all_users import (
    send_message_all_users_keyboard,
)
from ocrbot.keyboards.inline.admin_kbd.send_message_type import (
    send_message_type_keyboard,
)
from ocrbot.services.check_user_status import get_active_and_blocked_users
from ocrbot.states.states import FSMFillForm

user_messaging_router: Router = Router()


@user_messaging_router.message(
    F.text == "Сделать расылку 💬", AdminFilter(), flags={"throttling_key": "default"}
)
async def stand_by_message(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды для запуска процесса рассылки сообщения.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    await message.answer(
        text="Выберите тип сообщения для рассылки:",
        reply_markup=send_message_type_keyboard,
    )
    await state.set_state(FSMFillForm.message_to_users)


@user_messaging_router.callback_query(
    F.data.in_(["text_message", "image_with_text"]),
    StateFilter(FSMFillForm.message_to_users),
    AdminFilter(),
    flags={"throttling_key": "callback"},
)
async def get_message_type(query: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик выбора типа сообщения для рассылки.

    :param query: Объект CallbackQuery.
    :type query: aiogram.types.CallbackQuery
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    message_type = query.data
    if message_type == "text_message":
        await query.message.answer(text="Введите текст сообщения для рассылки.")
        await state.set_state(FSMFillForm.send_all_users)
    else:
        await query.message.answer(text="Отправьте картинку для рассылки.")
        await state.set_state(FSMFillForm.get_image)


@user_messaging_router.message(
    F.content_type == ContentType.PHOTO,
    StateFilter(FSMFillForm.get_image),
    AdminFilter(),
    flags={"throttling_key": "default"},
)
async def get_image(message: Message, state: FSMContext) -> None:
    """
    Обработчик получения изображения для рассылки.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    if message.photo:
        photo = message.photo[-1]
        await state.update_data(image=photo.file_id)
        await message.answer(text="Теперь введите текст, который будет под картинкой:")
        await state.set_state(FSMFillForm.send_all_users)
    else:
        await message.answer(text="Пожалуйста, отправьте картинку.")


@user_messaging_router.message(
    StateFilter(FSMFillForm.send_all_users),
    AdminFilter(),
    flags={"throttling_key": "default"},
)
async def confirm_message(message: Message, state: FSMContext) -> None:
    """
    Обработчик подтверждения сообщения для рассылки.

    :param message: Объект сообщения.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    data = await state.get_data()
    image_file_id = data.get("image")
    if image_file_id:
        admin_message = message.text
        await message.answer_photo(
            photo=image_file_id,
            caption=admin_message,
            reply_markup=send_message_all_users_keyboard,
        )
        await state.update_data(admin_message=admin_message)
    else:
        admin_message = message.text
        await message.answer(
            text=f"Ваше сообщение для рассылки:\n\n{admin_message}",
            reply_markup=send_message_all_users_keyboard,
            parse_mode="HTML"
        )
        await state.update_data(admin_message=admin_message)


@user_messaging_router.callback_query(
    F.data.in_(["cancel_send_message"]),
    StateFilter(FSMFillForm.send_all_users),
    AdminFilter(),
    flags={"throttling_key": "callback"},
)
async def cancel_message(
    query: Union[Message, CallbackQuery], state: FSMContext
) -> None:
    """
    Обработчик отмены рассылки сообщения.

    :param query: Объект CallbackQuery или Message.
    :type query: Union[aiogram.types.Message, aiogram.types.CallbackQuery]
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    message: Message = query if isinstance(query, Message) else query.message
    await message.answer(text="Успешно отменено!")
    await state.clear()


@user_messaging_router.callback_query(
    F.data.in_(["send_all"]),
    StateFilter(FSMFillForm.send_all_users),
    AdminFilter(),
    flags={"throttling_key": "callback"},
)
async def send_message_to_all_users(
    query: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    """
    Обработчик рассылки сообщения всем пользователям.

    :param query: Объект CallbackQuery.
    :type query: aiogram.types.CallbackQuery
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    :param bot: Объект бота.
    :type bot: aiogram.Bot
    """
    name: str = query.message.from_user.full_name
    data = await state.get_data()
    message_text = data.get("admin_message")
    image_file_id = data.get("image")
    _, active_users, _ = await get_active_and_blocked_users(bot)
    for user_id in set(active_users):
        try:
            if image_file_id:
                await bot.send_photo(
                    user_id,
                    photo=image_file_id,
                    caption=message_text,
                    parse_mode="HTML",
                )
            else:
                await bot.send_message(user_id, message_text, parse_mode="HTML")
            logging.info(f"The mailing was completed successfully to {user_id}!")
        except Exception as e:
            logging.info(f"Error when sending a message to a user {user_id}: {e}")

    await query.message.answer(text="Рассылка выполнена успешно!")
    logging.info(f"Administrator {name} has sent messages to users")
    await state.clear()
