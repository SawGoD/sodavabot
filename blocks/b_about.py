import os
import requests
import telegram
from blocks.u_handle_db import read_db_cell, write_db_cell
from blocks.u_common_func import ver, mod_fix
from blocks.s_path import filler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_changes(c_from=0, c_to=5):
    url = f"https://api.github.com/repos/SawGoD/sodavabot/commits?per_page=99"
    response = requests.get(url, headers={"Authorization": f"token {os.getenv('API_TOKEN_GIT')}"})
    output = "Последние изменения:\n\n"
    if response.status_code == 200:
        commits = response.json()
        c_max = int(len(commits))
        write_db_cell("menu_range", c_max, "last")
        commits = commits[c_from:c_to]
        i = read_db_cell('menu_range', 'last') - read_db_cell('menu_range', 'min') + 1
        for commit in commits:
            i -= 1
            commit_message = commit['commit']['message']
            commit_date = commit['commit']['author']['date'][:10].replace("-", r"\.")
            if commit['author'] is None:
                commit_author = commit['commit']['author']['name']
            else:
                commit_author = commit['author']['login']
                # commit_author = "2121"
            commit_url = commit['html_url']

            output += fr'''
 {i}\) *Обновление* - [{commit_date}]({commit_url}) от [{commit_author}](https://github.com/{commit_author}):
 *Изменения:* `{commit_message}`
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'''
        output += f"\nСтраница {read_db_cell('menu_range', 'page')} из {(c_max + 5 - 1) // 5}"
        output = output.replace('\n\n', '\n').replace('-', r'\-')
    return output


def update_menu_range(update, context, min_val, max_val, page_val):
    write_db_cell("menu_range", min_val, "min")
    write_db_cell("menu_range", max_val, "max")
    write_db_cell("menu_range", page_val, "page")
    bot_changes(update, context)


def bot_about(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    about = fr'''"SODA VA BOT"
        *Версия бота:* _{ver}_
        *Сейчас выбран:* _{read_db_cell("cur_pc")}_

Выберите ПК:'''
    keyboard = [[InlineKeyboardButton("👨🏻‍💻 Work", callback_data='sel_pc_1'),
                 InlineKeyboardButton("👩🏻‍💻 Home", callback_data='sel_pc_2')],
                [InlineKeyboardButton("🆕 Изменения", callback_data='bot_changes')],
                [InlineKeyboardButton("⚙️ Настройки", callback_data='bot_settings')],
                [InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🤖 *О боте*\n"+about.replace('.', r'\.'),
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def bot_settings(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton(f"📝 Логирование {'🟢' if read_db_cell('log_status') == 1 else '⚫'}",
                                      callback_data='logger')],
                [InlineKeyboardButton(f"🔔 Звуки {'🟢' if read_db_cell('sound_status') == 1 else '⚫'}",
                                      callback_data='sounds')],
                [InlineKeyboardButton("🔙 Назад", callback_data='bot_about'),
                 InlineKeyboardButton("Меню 🔝", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}⚙️ *Настройки*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def bot_changes(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)

    c_from_ = read_db_cell("menu_range", "min")
    c_to_ = read_db_cell("menu_range", "max")

    keyboard = [[InlineKeyboardButton("🔄", callback_data='bot_changes_upd')]]
    if c_from_ <= 0:
        keyboard.append([InlineKeyboardButton("▶️", callback_data='bot_changes_right')])
    elif c_to_ >= read_db_cell("menu_range", "last"):
        keyboard.append([InlineKeyboardButton("◀️", callback_data='bot_changes_left')])
    else:
        keyboard.append([InlineKeyboardButton("◀️", callback_data='bot_changes_left'),
                         InlineKeyboardButton("▶️", callback_data='bot_changes_right')])
    keyboard += [[InlineKeyboardButton("🔙 Назад", callback_data='bot_about'),
                 InlineKeyboardButton("Меню 🔝", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🆕️ *Изменения*{mod_fix()}\n{get_changes(c_from_, c_to_)}",
                            reply_markup=reply_markup,
                            disable_web_page_preview=True,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
