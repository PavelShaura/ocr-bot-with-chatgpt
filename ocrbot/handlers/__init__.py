from ocrbot.handlers.start.start import command_start_router
from ocrbot.handlers.user.get_photo import get_photo_router
from ocrbot.handlers.user.send_text import send_text_router
from ocrbot.handlers.user.shipping_to_chatgpt import shipping_to_gpt_router
from ocrbot.handlers.user.show_prompt import show_text_router
from ocrbot.handlers.user.own_text import own_text_router
from ocrbot.handlers.start.unexpected import unexpected_message_router
from ocrbot.handlers.admin.admin_menu import admin_menu_router
from ocrbot.handlers.admin.get_len_users import get_len_users_router
from ocrbot.handlers.admin.user_messaging import user_messaging_router

routers = [
    command_start_router,
    admin_menu_router,
    user_messaging_router,
    get_photo_router,
    send_text_router,
    shipping_to_gpt_router,
    show_text_router,
    own_text_router,
    get_len_users_router,
    unexpected_message_router,
]
