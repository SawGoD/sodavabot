import os

import telegram
from dotenv import load_dotenv

from blocks.s_path import filler
from blocks.u_common_func import clock
from blocks.u_handle_db import read_db_cell

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)


def log_form_tg(update, context, cmd=None, effect=True, alert=None):
    """
    Функция для логирования информации о пользователе и команде в Telegram.

    Аргументы:
    - update: Объект, содержащий информацию о событии в Telegram.
    - context: Контекст выполнения команды.
    - cmd: Команда, которую выполняет пользователь.
    - effect: Флаг, указывающий на наличие доступа к команде.
    - alert: Список команд, на которые нужно обратить внимание.

    Возвращает:
    - None
    """
    if read_db_cell("log_status") == 1:
        query = update.callback_query
        daten, timen = clock()
        username_ment = None
        if query and query.message:
            user_id = str(query.message.chat_id)
            query_log = str(query.data)
            if query.data in alert:
                username_ment = "FAKE_SGD"
                username_ment = f"@{username_ment}!".replace(
                    '_', r'\_').replace('*', r'\*').replace('!', r'\!')
            else:
                username_ment = ""
        else:
            user_id = str(update.message.chat_id)
            query_log = f"{cmd}"
            username_ment = ""
        user = update.effective_user
        if user.first_name is None:
            user_log = f"[{user.last_name}](tg://openmessage?user_id={user_id})"
        elif user.last_name is None:
            user_log = f"[{user.first_name}](tg://openmessage?user_id={user_id})"
        else:
            user_log = f"[{user.first_name} {user.last_name}](tg://openmessage?user_id={user_id})"
        time_log = timen
        log_message = fr'''
*Лог:* {username_ment}
    *• Пользователь:* {user_log}
    *• Время:* _{time_log}_
    *• Команда:* `{query_log}`
    *• Доступ:* _{"Есть" if effect else "Нет"}_
[{filler}](https://t.me/{context.bot.username})
'''
        if user_id in os.getenv('LOG_IGNORED_USERS'):
            pass
        else:
            bot.send_message(chat_id=os.getenv('LOG_OUTPUT'), text=log_message,
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)
    else:
        pass


def log_form_cmd(update, context, cmd=None, action=None, effect=True):
    """
    Функция для логирования информации о команде в консоли.

    Аргументы:
    - update: Объект, содержащий информацию о событии в Telegram.
    - context: Контекст выполнения команды.
    - cmd: Команда, которую выполняет пользователь.
    - action: Действие, связанное с командой.
    - effect: Флаг, указывающий на наличие доступа к команде.

    Возвращает:
    - None
    """
    daten, timen = clock()
    if update is None:
        if effect is True:
            print(f"Лог: {cmd} {action}|{timen}")
        elif effect is False:
            print(f"Лог: {cmd} не {action}|{timen}")
        else:
            print(f"Лог: {cmd} {effect}|Действие: {action}|{timen}")
    elif update:
        query = update.callback_query
        if query and query.message:
            user_id = str(query.message.chat_id)
            user = update.effective_user
            username = user.username
            query_log = str(query.data)
            print(
                f"Лог: @{username}/ID_{user_id} использует {query_log}|Доступ: {'Есть' if effect else 'Нет'}|{timen}")
        else:
            user_id = str(update.message.chat_id)
            user = update.effective_user
            username = user.username
            print(
                f"Лог: @{username}/ID_{user_id} использует {cmd}|Доступ: {'Есть' if effect else 'Нет'}|{timen}")
