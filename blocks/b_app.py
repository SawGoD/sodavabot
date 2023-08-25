import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blocks import s_path
from blocks.s_scripts_list import sdb_path
from blocks.u_common_func import user_input
from blocks.u_handle_db import read_db_cell


def app_menu(update, context):
    user_input(0, "none")
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🌐 Opera", callback_data='opera')],
                [InlineKeyboardButton("🕹️ Steam", callback_data='steam')]]
    if read_db_cell("pc", None) == 2:
        keyboard.append([InlineKeyboardButton(
            "🎨️ Stable Diffusion", callback_data='sdai')])
    keyboard += [[InlineKeyboardButton("🚀 Скрипты", callback_data='script')],
                 [InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📟 *Приложения*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def app_ui(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    app_on, app_off, app_sub, app_sub_text, app_ui_name = [0, 0, 0, 0, 0]
    app_name = read_db_cell("app_name", None)
    if app_name in s_path.app_data:
        app_on, app_off, app_sub, app_sub_text, app_ui_name = s_path.app_data[app_name].values(
        )

    keyboard = [[InlineKeyboardButton("✔ Запустить", callback_data=f'{app_on}')],

                [InlineKeyboardButton("❌ Закрыть", callback_data=f'{app_off}'),
                 InlineKeyboardButton(f"{app_sub_text}", callback_data=f'{app_sub}')],

                [InlineKeyboardButton("🔙 Назад", callback_data='apps'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}{app_ui_name}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def tabs_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔗 Отправить", callback_data='tab_send')],
                [InlineKeyboardButton("◀️", callback_data='tab_left'),
                 InlineKeyboardButton("▶️", callback_data='tab_right')],
                # [InlineKeyboardButton("↩️", callback_data='tab_prev'),
                #  InlineKeyboardButton("↪️", callback_data='tab_next')],

                [InlineKeyboardButton(
                    "👁‍🗨 Инкогнито", callback_data='opi_on')],

                [InlineKeyboardButton("❌ Закрыть", callback_data='tab_off'),
                 InlineKeyboardButton("🔖 Вернуть", callback_data='tab_return')],

                [InlineKeyboardButton("🔙 Назад", callback_data='opera'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📑 *Вкладки*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def games_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔗 Скачать игру", callback_data='game_send')],
                [InlineKeyboardButton("🚫 Отмена", callback_data='game_canc')],

                [InlineKeyboardButton("🔙 Назад", callback_data='steam'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📑 *Игры*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def sdai_links_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔗 Local", url=f'{read_db_cell("sd_link_local", None)}')],
                [InlineKeyboardButton(
                    "🔗 Share", url=f'{read_db_cell("sd_link_share", None)}')],

                [InlineKeyboardButton("🔙 Назад", callback_data='sdai'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🔗 *Ссылки*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def scripts_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🤕 Escape From Tarkov", callback_data='scr_eft')],
                # [InlineKeyboardButton("0️⃣ Holder [x]", callback_data='scr_idk')],
                [InlineKeyboardButton("🔙 Назад", callback_data='apps'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🚀 *Скрипты*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def scr_eft_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [
        [InlineKeyboardButton(f"1️⃣ Buyer [{read_db_cell('seft_1_set', 'value', filename=sdb_path)}] "
                              f"{'🟢' if read_db_cell('script_eft_1', None, filename=sdb_path) == 1 else '⚫'}",
                              callback_data='scr_eft_1')]]
    if read_db_cell("script_eft_1", None, filename=sdb_path) == 1:
        keyboard.append([InlineKeyboardButton("➖", callback_data='eft_1_down'),
                        InlineKeyboardButton("5", callback_data='eft_1_5'),
                        InlineKeyboardButton("➕", callback_data='eft_1_up')])
    keyboard += [
        [InlineKeyboardButton(f"2️⃣ Simple Clicker "
                              f"{'🟢' if read_db_cell('script_eft_2', None, filename=sdb_path) == 1 else '⚫'}",
                              callback_data='scr_eft_2')],
        [InlineKeyboardButton(f"3️⃣ [x] {'🟢' if read_db_cell('script_eft_3', None, filename=sdb_path) == 1 else '⚫'}",
                              callback_data='scr_eft_3')],
        [InlineKeyboardButton("⭕ Выключить всё", callback_data='scr_eft_off')],
        [InlineKeyboardButton("🔙 Назад", callback_data='script'),
         InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🤕 *Escape From Tarkov*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
