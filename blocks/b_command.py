import os
import re
import threading
import time

import telegram
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blocks import u_send_logs
from blocks.s_path import filler
from blocks.u_common_func import clock, restart_bot

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)


def start(update, context):
    user_id = str(update.message.chat_id)
    user = update.effective_user
    username = user.username
    daten, timen = clock()
    if user_id not in os.getenv('ALLOWED_USERS'):
        context.bot.send_message(chat_id=user_id, text="У Вас нет доступа")
        u_send_logs.log_form_cmd(update, context, effect=False, cmd="start")
        u_send_logs.log_form_tg(update, context, effect=False, cmd="start")
    else:
        u_send_logs.log_form_cmd(update, context, effect=True, cmd="start")
        u_send_logs.log_form_tg(update, context, effect=True, cmd="start")
        context.bot.send_message(
            chat_id=user_id, text=f"_Подключено_", parse_mode=telegram.ParseMode.MARKDOWN)
        keyboard = [[InlineKeyboardButton("🖥 Компьютер", callback_data='computer')],
                    [InlineKeyboardButton(
                        "📟 Приложения", callback_data='apps')],
                    [InlineKeyboardButton("🤖 О боте", callback_data='bot_about')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=user_id, text=f'{filler}🔝 *Меню*',
                                 reply_markup=reply_markup,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)


def restart(update, context):
    user_id = str(update.message.chat_id)
    user = update.effective_user
    username = user.username
    daten, timen = clock()
    if user_id not in os.getenv('ALLOWED_USERS'):
        context.bot.send_message(chat_id=user_id, text="У Вас нет доступа")
        u_send_logs.log_form_cmd(update, context, effect=False, cmd="restart")
        u_send_logs.log_form_tg(update, context, effect=False, cmd="restart")
    else:
        u_send_logs.log_form_cmd(update, context, effect=True, cmd="restart")
        u_send_logs.log_form_tg(update, context, effect=True, cmd="restart")
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        restart_bot()


def get_threads(update, context):
    user_id = str(update.message.chat_id)
    user = update.effective_user
    username = user.username
    daten, timen = clock()
    all_threads = threading.enumerate()
    mes = ""
    for thread in all_threads:
        if ":dispatcher" not in thread.name and ":worker" not in thread.name and ":updater" not in thread.name and "APScheduler" not in thread.name and "MainThread" not in thread.name:
            mes += (f"*Поток:* `{thread.name}` \n")
    mes = re.sub(r'[-()+:]', lambda x: '\\' + x.group(), mes)
        # print(f"Поток: {thread.name}")
    # mes = [text.encode('utf-8').decode('utf-8') for text in mes]

    if user_id not in os.getenv('ADMIN_USERS'):
        context.bot.send_message(chat_id=user_id, text="У Вас нет доступа")
        u_send_logs.log_form_cmd(
            update, context, effect=False, cmd="get_threads")
        u_send_logs.log_form_tg(
            update, context, effect=False, cmd="get_threads")
    else:
        # context.bot.send_message(chat_id=user_id, text=mes,)
        message = bot.send_message(chat_id=update.effective_chat.id, text=mes,
                                   parse_mode=telegram.ParseMode.MARKDOWN_V2)
        keyboard = [[InlineKeyboardButton(
            "Удалить", callback_data=f"text_del:{message.message_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            reply_markup=reply_markup)
        u_send_logs.log_form_cmd(
            update, context, effect=True, cmd="get_threads")
        u_send_logs.log_form_tg(
            update, context, effect=True, cmd="get_threads")
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
