import os

from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from bot_callbacks.computer_callbacks import *
from bot_message_func import edit_bot_message
from definitions.services.main_menu import main_menu as main_menu_interface
from definitions.services.menu_controls import menu_controls
from utils import *


def main_keyboard(access: bool = True) -> list:
    if access:
        main_keyboard = [
            [
                InlineKeyboardButton(main_menu_interface.apps, callback_data="apps_callback"),
                InlineKeyboardButton(main_menu_interface.computer, callback_data="computer_callback"),
            ],
            [
                InlineKeyboardButton(main_menu_interface.settings, callback_data="settings_callback"),
            ],
        ]
    else:
        main_keyboard = [[InlineKeyboardButton(menu_controls.update, callback_data="upd_callback")]]
    return main_keyboard


async def main_menu(update: Update, context: ContextTypes) -> None:
    chat_data = update.message or update.callback_query.message
    user_id = chat_data.chat_id
    if str(user_id) in os.getenv("ALLOWED_USERS"):
        flag = True
        title = main_menu_interface.title
    else:
        flag = False
        title = main_menu_interface.no_access
    text = f"*{title}*" + mod_fix()

    reply_markup = main_keyboard(access=flag)
    await edit_bot_message(update, context, message_text=text, reply_markup=reply_markup)


async def buttons_handler(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    buttons_deps_dict = read_json(filename="buttons_deps_dict")
    buttons_heads_dict = (
        "goto_main_layer",
        "goto_second_layer",
        "goto_computer_layer",
    )
    btns_n_actns_heads_dict = ("goto_custom_behavior",)
    print("\n" * 3)
    print(query.data)
    for menu in btns_n_actns_heads_dict:
        if query.data in buttons_deps_dict[menu]:
            await eval(buttons_deps_dict[menu][query.data])
            print("Keys changed")
            break
    for menu in buttons_heads_dict:
        if query.data in buttons_deps_dict[menu]:
            await eval(buttons_deps_dict[menu][query.data])(update, context)
            await set_to_default_state()
            write_json(
                query.data[:query.data.index("_callback")],
                "menu_data",
                "current_location",
                filename="fleeting_data",
            )
            print("Menu changed")
            break
