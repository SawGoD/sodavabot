import os

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blocks import u_send_logs
from blocks.s_path import filler
from blocks.u_common_func import clock, restart_bot


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
