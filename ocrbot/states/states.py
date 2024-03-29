from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    rewritten_prompt = State()
    message_to_users = State()
    send_all_users = State()
    get_image = State()
    provider_being_selected = State()
