import os

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot_callbacks.buttons_handler import main_keyboard
from bot_message_func import edit_bot_message, send_bot_message
from utils import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_data = update.message
    user_id = chat_data.chat_id
    try:
        await context.bot.delete_message(
            chat_id=user_id, message_id=chat_data.message_id
        )
    except:
        pass
    titles_dict = read_json(filename="titles_dict")
    if str(user_id) in os.getenv("ALLOWED_USERS"):
        title = titles_dict["main_menu"]["title"]
        text = f"*{title}*" + mod_fix()
        reply_markup = InlineKeyboardMarkup(main_keyboard(access=True))
        await send_bot_message(
            update, context, message_text=text, reply_markup=reply_markup
        )
    else:
        title = titles_dict["main_menu"]["title_no_access"]
        text = f"*{title}*" + mod_fix()
        reply_markup = InlineKeyboardMarkup(main_keyboard(access=False))
        await send_bot_message(
            update, context, message_text=text, reply_markup=reply_markup
        )


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_data = update.message
    user_id = chat_data.chat_id
    if str(user_id) not in os.getenv("ALLOWED_USERS"):
        await context.bot.send_message(chat_id=user_id, text="У Вас нет доступа")
    else:
        message_id = chat_data.message_id
        await context.bot.delete_message(chat_id=user_id, message_id=message_id)
        restart_bot()
