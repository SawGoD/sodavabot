import os
import re
import s_path
import s_scripts_list
import telegram
import pyautogui
import subprocess
import pyperclip
import sys
import plyer
import time
import requests
from telegram.error import NetworkError, Unauthorized
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


s_path.ver_greet()
s_path.thread_speed_test.start()
s_scripts_list.thread_script_eft_1.start()
s_scripts_list.thread_script_eft_2.start()
s_scripts_list.thread_script_eft_3.start()

user_data = {}
sdb_path = s_scripts_list.sdb_path
s_con_path = "s_connection.json"

TOKEN = '6163227559:AAGBltGEjoq323lnwKNDozUZ9JxS0UGBuZs'
bot = telegram.Bot(token=TOKEN)


def start(update, context):
    user_id = str(update.message.chat_id)
    user = update.effective_user
    username = user.username
    if user_id not in s_path.read_db_cell("users"):
        context.bot.send_message(chat_id=user_id, text="У вас нет доступа")
        print(f"@{username}/ID_{user_id} не имеет доступа|{s_path.now_time}")
    else:
        print(f"@{username}/ID_{user_id} успешно подключился|{s_path.now_time}")
        context.bot.send_message(chat_id=user_id, text=f"_Подключено_", parse_mode=telegram.ParseMode.MARKDOWN)
        keyboard = [[InlineKeyboardButton("🖥 Компьютер", callback_data='computer')],
                    [InlineKeyboardButton("📟 Приложения", callback_data='apps')],
                    [InlineKeyboardButton("🤖 О боте", callback_data='about_bot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=user_id, text=f'{s_path.filler}🔝 *Меню*',
                                 reply_markup=reply_markup,
                                 parse_mode=telegram.ParseMode.MARKDOWN)
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)


def restart(update, context):
    user_id = str(update.message.chat_id)
    user = update.effective_user
    username = user.username
    if user_id not in s_path.read_db_cell("users"):
        context.bot.send_message(chat_id=user_id, text="У вас нет доступа")
        print(f"@{username}/ID_{user_id} не имеет доступа к перезапуску|{s_path.now_time}")
    else:
        print(f"@{username}/ID_{user_id} перезапускает бота|{s_path.now_time}")
        plyer.notification.notify \
            (message=f"@{username} перезапускает бота\n{s_path.now_time}",
             app_icon=fr'.\resource\sample.ico',
             title='Перезапуск', )
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        python = sys.executable
        os.execv(python, [python, fr".\soda_va_bot.py"])


def computer_menu(update, context):
    s_path.user_input(0, "none")
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔂 Мультимедиа", callback_data='multi'),
                 InlineKeyboardButton("🔒 VPN", callback_data='vpn')],
                [InlineKeyboardButton("📷 Экран", callback_data='screen'),
                 InlineKeyboardButton("📋 Буфер обмена", callback_data='clipboard')],
                [InlineKeyboardButton("⚠ Питание", callback_data='pc')],
                [InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🖥 *Компьютер*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def about_text(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    about = f'''"SODA VA BOT"
        *Версия бота:* _{s_path.ver}_
        *Сейчас выбран:* _{s_path.read_db_cell("cur_pc")}_

Выберите ПК:'''
    keyboard = [[InlineKeyboardButton("👨🏻‍💻 Work", callback_data='sel_pc_1'),
                 InlineKeyboardButton("👩🏻‍💻 Home", callback_data='sel_pc_2')],
                [InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🤖 *О б1оте*\n {about}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def multi_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    s_path.get_volume()
    keyboard = [
        [InlineKeyboardButton(f"🌀 {s_path.read_db_cell('volume', 'head_h')} "
                              f"{'🟢' if s_path.read_db_cell('output_device') == 'headphones_h' else '⚫'}",
                              callback_data='set_dev_head_h'),
         InlineKeyboardButton(f"{'🟢' if s_path.read_db_cell('output_device') == 'monitor_r' else '⚫'} "
                              f"{s_path.read_db_cell('volume', 'mon_r')} 🖥",
                              callback_data='set_dev_mon_r')]]
    if s_path.read_db_cell("pc", None) == 1:
        keyboard.append([InlineKeyboardButton(f"{'🟢' if s_path.read_db_cell('output_device') == 'monitor_l' else '⚫'} "
                                              f"{s_path.read_db_cell('volume', 'mon_l')} 🖥",
                                              callback_data='set_dev_mon_l')])
    elif s_path.read_db_cell("pc", None) == 2:
        keyboard.append([InlineKeyboardButton(
            f"🎸 {s_path.read_db_cell('volume', 'head_s')} "
            f"{'🟢' if s_path.read_db_cell('output_device') == 'headphones_s' else '⚫'}",
            callback_data='set_dev_head_s'),
            InlineKeyboardButton(
                f"{'🟢' if s_path.read_db_cell('output_device') == 'headphones_a' else '⚫'} "
                f"{s_path.read_db_cell('volume', 'head_a')} 🩸",
                callback_data='set_dev_head_a')])
    keyboard += [
                [InlineKeyboardButton("⏪", callback_data='multi_pull'),
                 InlineKeyboardButton("⏯", callback_data='multi_on_off'),
                 InlineKeyboardButton("⏩", callback_data='multi_force')],

                [InlineKeyboardButton("⏮", callback_data='multi_prev'),
                 InlineKeyboardButton("50", callback_data="vol_50"),
                 InlineKeyboardButton("⏭", callback_data='multi_next')],

                [InlineKeyboardButton("➖", callback_data='vol_down'),
                 InlineKeyboardButton("-10", callback_data="vol_down10"),
                 InlineKeyboardButton(f"{'🔇' if s_path.read_db_cell('volume_status') == 0 else '🔊'}",
                                      callback_data='vol_on_off'),
                 InlineKeyboardButton("+10", callback_data="vol_up10"),
                 InlineKeyboardButton("➕", callback_data='vol_up')],

                [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                 InlineKeyboardButton("Меню 🔝", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🔂 *Мультимедиа*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def pc_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [
                # [InlineKeyboardButton(f"⚫🟢 Состояние LED [x] ", callback_data='led_upd')],
                [InlineKeyboardButton("🔄", callback_data='pc_reb'),
                 InlineKeyboardButton("💤", callback_data='pc_hyb'),
                 InlineKeyboardButton("⭕", callback_data='pc_off')],
                [InlineKeyboardButton("🚫 Отмена", callback_data='pc_canc')],
                [InlineKeyboardButton("🙈", callback_data='mon_off')],

                [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}⚠ *Питание*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def screen_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [
        [InlineKeyboardButton("◼️", callback_data='scrn_full'),
         InlineKeyboardButton("◾️", callback_data='scrn_mon'),
         InlineKeyboardButton("▪️", callback_data='scrn_app')],
        # [InlineKeyboardButton("➖ Удалить", callback_data='scrn_del')],

        [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
         InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📷 *Экран*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def clipboard_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    # clipboard_content = pyperclip.paste()
    keyboard = [
        [InlineKeyboardButton("📤 Отправить", callback_data='get_paste'),
         InlineKeyboardButton("Получить 📥", callback_data='get_copy')],
        [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
         InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📋 *Буфер обмена*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def app_menu(update, context):
    s_path.user_input(0, "none")
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🌐 Opera", callback_data='opera')],
                [InlineKeyboardButton("🕹️ Steam", callback_data='steam')]]
    if s_path.read_db_cell("pc", None) == 2:
        keyboard.append([InlineKeyboardButton("🎨️ Stable Diffusion", callback_data='sdai')])
    keyboard += [[InlineKeyboardButton("🚀 Скрипты", callback_data='script')],
                 [InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📟 *Приложения*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def app_ui(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    app_on, app_off, app_sub, app_sub_text, app_ui_name = [0, 0, 0, 0, 0]
    app_name = s_path.read_db_cell("app_name", None)
    if app_name in s_path.app_data:
        app_on, app_off, app_sub, app_sub_text, app_ui_name = s_path.app_data[app_name].values()

    keyboard = [[InlineKeyboardButton("✔ Запустить", callback_data=f'{app_on}')],

                [InlineKeyboardButton("❌ Закрыть", callback_data=f'{app_off}'),
                 InlineKeyboardButton(f"{app_sub_text}", callback_data=f'{app_sub}')],

                [InlineKeyboardButton("🔙 Назад", callback_data='apps'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}{app_ui_name}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def tabs_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔗 Отправить", callback_data='tab_send')],
                [InlineKeyboardButton("◀️", callback_data='tab_pull'),
                 InlineKeyboardButton("▶️", callback_data='tab_force')],
                # [InlineKeyboardButton("↩️", callback_data='tab_prev'),
                #  InlineKeyboardButton("↪️", callback_data='tab_next')],

                [InlineKeyboardButton("👁‍🗨 Инкогнито", callback_data='opi_on')],

                [InlineKeyboardButton("❌ Закрыть", callback_data='tab_off'),
                 InlineKeyboardButton("🔖 Вернуть", callback_data='tab_return')],

                [InlineKeyboardButton("🔙 Назад", callback_data='opera'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📑 *Вкладки*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def games_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔗 Скачать игру", callback_data='game_send')],
                [InlineKeyboardButton("🚫 Отмена", callback_data='game_canc')],

                [InlineKeyboardButton("🔙 Назад", callback_data='steam'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}📑 *Игры*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def sdai_links_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔗 Local", url=f'{s_path.read_db_cell("sd_link_local", None)}')],
                [InlineKeyboardButton("🔗 Share", url=f'{s_path.read_db_cell("sd_link_share", None)}')],

                [InlineKeyboardButton("🔙 Назад", callback_data='sdai'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🔗 *Ссылки*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def scripts_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🤕 Escape From Tarkov", callback_data='scr_eft')],
                # [InlineKeyboardButton("0️⃣ Holder [x]", callback_data='scr_idk')],
                [InlineKeyboardButton("🔙 Назад", callback_data='apps'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🚀 *Скрипты*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def scr_eft_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [
        [InlineKeyboardButton(f"1️⃣ Buyer [{s_path.read_db_cell('seft_1_set', 'value', sdb_path)}] "
                              f"{'🟢' if s_path.read_db_cell('script_eft_1', None, sdb_path) == 1 else '⚫'}",
                              callback_data='scr_eft_1')]]
    if s_path.read_db_cell("script_eft_1", None, sdb_path) == 1:
        keyboard.append([InlineKeyboardButton("➖", callback_data='eft_1_down'),
                        InlineKeyboardButton("5", callback_data='eft_1_5'),
                        InlineKeyboardButton("➕", callback_data='eft_1_up')])
    keyboard += [
        [InlineKeyboardButton(f"2️⃣ Simple Clicker {'🟢' if s_path.read_db_cell('script_eft_2', None, sdb_path) == 1 else '⚫'}",
                              callback_data='scr_eft_2')],
        [InlineKeyboardButton(f"3️⃣ [x] {'🟢' if s_path.read_db_cell('script_eft_3', None, sdb_path) == 1 else '⚫'}",
                              callback_data='scr_eft_3')],
        [InlineKeyboardButton("⭕ Выключить всё", callback_data='scr_eft_off')],
        [InlineKeyboardButton("🔙 Назад", callback_data='script'),
         InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🤕 *Escape From Tarkov*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def vpn_menu(update, context):
    # инициализируем переменные для первого запуска кода
    last_modified = 0
    last_sp_avg = 0

    # проверяем, изменился ли файл speed.txt с момента последнего запуска кода
    file_path = fr'{s_path.DEFPATH}\data\{s_con_path}'
    if os.path.exists(file_path):
        modified_time = os.path.getmtime(file_path)
        if modified_time != last_modified:
            # файл изменился, нужно пересчитать значение скорости
            download = ((s_path.read_db_cell("download", 'bytes', s_con_path) * 8) /
                        (s_path.read_db_cell("download", 'elapsed', s_con_path) * 1000))
            upload = ((s_path.read_db_cell("upload", 'bytes', s_con_path) * 8) /
                      (s_path.read_db_cell("upload", 'elapsed', s_con_path) * 1000))
            sp_avg = round((download + upload) / 2, 2)
            in_ip = s_path.read_db_cell("interface", 'internalIp', s_con_path)
            ex_ip = s_path.read_db_cell("interface", 'externalIp', s_con_path)
            last_modified = modified_time
        else:
            # файл не изменился, возвращаем предыдущее значение скорости
            sp_avg = last_sp_avg
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

    # сохраняем текущее значение скорости в переменной для следующей проверки
    last_sp_avg = sp_avg
    query = update.callback_query
    user_id = str(query.message.chat_id)
    about = f'''[Данные сети]({s_path.read_db_cell("result", 'url', s_con_path)}):
        _Задержка:_ `{round(s_path.read_db_cell("ping", 'latency', s_con_path), 2)}ms`
        _Внутренний IP:_ `{s_path.read_db_cell("interface", 'internalIp',s_con_path)}`
        _Внешний IP:_ `{s_path.read_db_cell("interface", 'externalIp',s_con_path)}`
        '''
    keyboard = [[InlineKeyboardButton(f"🇩🇪 DE {'🟢' if s_path.read_db_cell('vpn_status') == 'DE' else '⚫'}",
                                      callback_data='vpn_1'),
                 InlineKeyboardButton(f"🇹🇷 TR {'🟢' if s_path.read_db_cell('vpn_status') == 'TR' else '⚫'}",
                                      callback_data='vpn_2'),
                 InlineKeyboardButton(f"🇱🇹 LT {'🟢' if s_path.read_db_cell('vpn_status') == 'LT' else '⚫'}",
                                      callback_data='vpn_3')],

                [InlineKeyboardButton(f"📶 Mbps: {sp_avg}", callback_data='con_speed'),
                 InlineKeyboardButton("⭕ Выключить ", callback_data='vpn_off')],

                [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                 InlineKeyboardButton("🔝 Menu", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{s_path.filler}🔒 *VPN* \n{about}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)


def set_output_device(device, query):
    os.system(f'{s_path.SETDEVDEF} {device[0]}')
    os.system(f'{s_path.SETDEVDEFCOMM} {device[0]}')
    device_name = ''
    if s_path.read_db_cell("pc", None) == 1:
        device_name = "headphones_h" if device == s_path.SPEAK_HEAD_H \
            else "monitor_r" if device == s_path.SPEAK_MON_R \
            else "monitor_l" if device == s_path.SPEAK_MON_L \
            else "none"
        current_markup = query.message.reply_markup
        current_markup.inline_keyboard[0][
            0].text = f"🌀 {s_path.read_db_cell('volume', 'head_h')} {'🟢' if device == s_path.SPEAK_HEAD_H else '⚫️'}"
        current_markup.inline_keyboard[0][
            1].text = f"{'🟢' if device == s_path.SPEAK_MON_R else '⚫️'} {s_path.read_db_cell('volume', 'mon_r')} 🖥"
        current_markup.inline_keyboard[1][
            0].text = f"{'🟢' if device == s_path.SPEAK_MON_L else '⚫️'} {s_path.read_db_cell('volume', 'mon_l')} 🖥"
        query.edit_message_reply_markup(reply_markup=current_markup)
    elif s_path.read_db_cell("pc", None) == 2:
        device_name = "headphones_h" if device == s_path.SPEAK_HEAD_H \
            else "headphones_s" if device == s_path.SPEAK_HEAD_S \
            else "headphones_a" if device == s_path.SPEAK_HEAD_A \
            else "monitor_r" if device == s_path.SPEAK_MON_R \
            else "none"
        current_markup = query.message.reply_markup
        current_markup.inline_keyboard[0][
            0].text = f"🌀 {s_path.read_db_cell('volume', 'head_h')} {'🟢' if device == s_path.SPEAK_HEAD_H else '⚫️'}"
        current_markup.inline_keyboard[0][
            1].text = f"{'🟢' if device == s_path.SPEAK_MON_R else '⚫️'} {s_path.read_db_cell('volume', 'mon_r')} 🖥"
        current_markup.inline_keyboard[1][
            0].text = f"🎸 {s_path.read_db_cell('volume', 'head_s')} {'🟢' if device == s_path.SPEAK_HEAD_S else '⚫️'}"
        current_markup.inline_keyboard[1][
            1].text = f"{'🟢' if device == s_path.SPEAK_HEAD_A else '⚫️'} {s_path.read_db_cell('volume', 'head_a')} 🩸"
        query.edit_message_reply_markup(reply_markup=current_markup)
    s_path.write_db_cell("output_device", device_name)


def take_screenshot(key, context, update):
    if not os.path.exists(s_path.SHAREX):
        os.makedirs(s_path.SHAREX)
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
    for file_name in os.listdir(s_path.SHAREX):
        file_path = os.path.join(s_path.SHAREX, file_name)
        os.remove(file_path)
    pyautogui.keyDown(key)
    pyautogui.press('prntscrn')
    pyautogui.keyUp(key)
    time.sleep(0.15)
    for filename in os.listdir(s_path.SHAREX):
        photo_message = context.bot.send_photo(chat_id=update.effective_chat.id,
                                               photo=open(os.path.join(s_path.SHAREX, filename), 'rb'),
                                               reply_markup=InlineKeyboardMarkup([[
                                                   InlineKeyboardButton(text="Удалить",
                                                                        callback_data=f"scrn_del:{filename}")
                                               ]]))
        context.user_data[filename] = photo_message.message_id  # сохраняем ID сообщения в UserDict


def button(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)

    if query.data in s_path.menu_buttons:
        eval(s_path.menu_buttons[query.data])
    elif query.data in s_path.multi_act:
        eval(s_path.multi_act[query.data])
    elif query.data in s_path.apps_os_act:
        os.system(s_path.apps_os_act[query.data])
    elif query.data in s_path.tabs_hotkeys:
        pyautogui.hotkey(*s_path.tabs_hotkeys[query.data])
        pass
    elif query.data in s_path.scr_keys:
        option = s_path.scr_keys[query.data]
        take_screenshot(option, context, update)
    elif query.data in s_path.dict_text_cmd:
        command = s_path.dict_text_cmd[query.data]
        query.answer(text=command['text'])
        os.system(command['cmd'])

    elif query.data in s_path.dict_text_cell:
        command = s_path.dict_text_cell[query.data]
        query.answer(text=command['text'])
        s_path.user_input(1, command['cell'])

    elif query.data in s_path.vpn_paths:
        query.answer(text='Подключение через 5 секунд')
        os.system(f'{s_path.VPN_TO} {s_path.vpn_paths[query.data]}')
        if query.data == 'vpn_1':
            s_path.write_db_cell("vpn_status", "DE")
        elif query.data == 'vpn_2':
            s_path.write_db_cell("vpn_status", "TR")
        elif query.data == 'vpn_3':
            s_path.write_db_cell("vpn_status", "LT")
        vpn_menu(update, context)

    elif query.data == 'vol_down10':
        query.answer(text='Громкость уменьшена на 10')
        for _ in range(5):
            pyautogui.press("volumedown")
        multi_menu(update, context)
        pass
    elif query.data == 'vol_50':
        query.answer(text='Громкость: 50%')
        os.system(fr'"{s_path.SETVOL}" 50')
        multi_menu(update, context)
        pass
    elif query.data == 'vol_up10':
        query.answer(text='Громкость увеличена на 10')
        for _ in range(5):
            pyautogui.press("volumeup")
        multi_menu(update, context)
        pass
    elif query.data == 'vol_up':
        query.answer(text='Громкость увеличена на 2')
        pyautogui.press("volumeup")
        multi_menu(update, context)
        pass
    elif query.data == 'vol_down':
        query.answer(text='Громкость уменьшена на 2')
        pyautogui.press("volumedown")
        multi_menu(update, context)
        pass
    elif query.data == 'vol_on_off':
        new_status = 0 if s_path.read_db_cell("volume_status") == 1 else 1
        s_path.write_db_cell("volume_status", new_status)
        current_markup = query.message.reply_markup
        if new_status == 0:
            current_markup.inline_keyboard[4][2].text = f"🔇"
            # Действие по выключению звука
            pyautogui.press("volumemute")
        else:
            current_markup.inline_keyboard[4][2].text = f"🔊"
            pyautogui.press("volumemute")
        query.edit_message_reply_markup(reply_markup=current_markup)
        pass

    elif query.data.startswith(('scrn_del:', 'text_del:')):
        if query.data.startswith('scrn_del:'):
            file_name = query.data.split(':')[1]  # получаем название файла скриншота из callback_data
            message_id = context.user_data.get(file_name)  # получаем ID сообщения из UserDict
            if message_id:
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
                del context.user_data[file_name]  # удаляем запись из UserDict
            os.remove(os.path.join(s_path.SHAREX, file_name))  # удаляем файл скриншота

        elif query.data.startswith('text_del:'):
            message_id = int(query.data.split(":")[1])
            bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)

    elif query.data == 'get_copy':
        clipboard_content = pyperclip.paste()
        message_text = f"`{clipboard_content}`"
        # message_text += "Нажмите кнопку \"Удалить\", чтобы удалить это сообщение"
        message = bot.send_message(chat_id=update.effective_chat.id, text=message_text,
                                   parse_mode=telegram.ParseMode.MARKDOWN)
        keyboard = [[InlineKeyboardButton("Удалить", callback_data=f"text_del:{message.message_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            reply_markup=reply_markup)

    elif query.data == 'con_speed':
        query.answer(text='Автообновление каждые 30 секунд')
        vpn_menu(update, context)
        pass
    elif query.data == 'vpn_off':
        query.answer(text='Отключение через 3 секунды')
        os.system(f'{s_path.VPN_OFF}')
        s_path.write_db_cell("vpn_status", "off")
        vpn_menu(update, context)

    elif query.data in ['opera', 'steam', 'sdai']:
        s_path.write_db_cell("app_name", query.data, None)
        app_ui(update, context)
    elif query.data == 'st_on':
        subprocess.Popen(f'{s_path.STEAM}/steam.exe')

    elif query.data == 'sdai_off':
        # os.system('taskkill /f /PID 8989898')
        print("off - ne rabotaer")

    elif query.data == 'scr_eft_1':
        status = 0 if s_path.read_db_cell("script_eft_1", None, sdb_path) == 1 else 1
        s_path.write_db_cell(f"script_eft_1", status, None, sdb_path)
        scr_eft_menu(update, context)
    elif query.data == 'eft_1_down':
        x = s_path.read_db_cell("seft_1_set", 'value', sdb_path)
        y = x - 1
        s_path.write_db_cell("seft_1_set", y, "value", "s_scripts_db.json")
        scr_eft_menu(update, context)
    elif query.data == "eft_1_5":
        s_path.write_db_cell("seft_1_set", 5, "value", "s_scripts_db.json")
        scr_eft_menu(update, context)
    elif query.data == 'eft_1_up':
        x = s_path.read_db_cell("seft_1_set", 'value', sdb_path)
        y = x + 1
        s_path.write_db_cell("seft_1_set", y, "value", "s_scripts_db.json")
        scr_eft_menu(update, context)
    elif query.data == 'scr_eft_2':
        status = 0 if s_path.read_db_cell("script_eft_2", None, sdb_path) == 1 else 1
        s_path.write_db_cell(f"script_eft_2", status, None, sdb_path)
        scr_eft_menu(update, context)
    elif query.data == 'scr_eft_3':
        status = 0 if s_path.read_db_cell("script_eft_3", None, sdb_path) == 1 else 1
        s_path.write_db_cell(f"script_eft_3", status, None, sdb_path)
        scr_eft_menu(update, context)
    elif query.data == 'scr_eft_off':
        for i in range(1, 4):
            s_path.write_db_cell(f"script_eft_{i}", 0, sdb_path)
        scr_eft_menu(update, context)

    elif query.data == 'sel_pc_1':
        s_path.write_db_cell("pc", 1)
        s_path.write_db_cell("cur_pc", "👨🏻‍💻 Рабочий ПК")
        query.answer(text='Принудительный перезапуск')
        about_text(update, context)
        python = sys.executable
        os.execv(python, [python, fr".\soda_va_bot.py"])
    elif query.data == 'sel_pc_2':
        s_path.write_db_cell("pc", 2)
        s_path.write_db_cell("cur_pc", "👩🏻‍💻 Домашний ПК")
        query.answer(text='Принудительный перезапуск')
        about_text(update, context)
        python = sys.executable
        os.execv(python, [python, fr".\soda_va_bot.py"])

    elif query.data == 'mmenu':
        s_path.user_input(0, "none")
        keyboard = [[InlineKeyboardButton("🖥 Компьютер", callback_data='computer')],
                    [InlineKeyboardButton("📟 Приложения", callback_data='apps')],
                    [InlineKeyboardButton("🤖 О боте", callback_data='about_bot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.edit_message_text(chat_id=user_id, message_id=query.message.message_id,
                                      text=f'{s_path.filler}🔝 *Меню*',
                                      reply_markup=reply_markup,
                                      parse_mode=telegram.ParseMode.MARKDOWN)


def handle_text(update, context):
    if s_path.read_db_cell("waiting_input") == 1:
        message_text = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        if s_path.read_db_cell("handle_type") == 'links':
            urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', message_text)
            message_text = urls[0]
            os.system(f'{s_path.BROWSER} {message_text}')
        elif s_path.read_db_cell("handle_type") == 'clipboard':
            pyperclip.copy(message_text)
        elif s_path.read_db_cell("handle_type") == 'game':
            def get_appid(name):
                url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    app_list = data["applist"]["apps"]
                    for app in app_list:
                        if app["name"].lower() == name.lower():
                            return app["appid"]
                return None

            # st_password = message_text[:12]
            st_password = s_path.true_try
            # game_name = message_text[13:-6]
            game_name = message_text[:-6]
            code_2fa = message_text[-5:]
            appid = get_appid(game_name)
            if appid:
                print(f"AppID игры {game_name}: {appid}")
                # install_dir = fr'"{s_path.STEAM}\steamapps\common\"'
                install_dir = r'C:\Own\test'
                cmd = f'"{s_path.STEAMCMD}" +force_install_dir {install_dir} +login flay_exe {str(st_password)} {str(code_2fa)} +app_update {str(appid)} validate +quit'
                # lets_install = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                os.system(cmd)
            else:
                print(f"Игра {game_name} не найдена")
    else:
        # обрабатываем сообщение как обычно
        pass


def main():
    with open(r'.\logs\error_py.txt', 'w', encoding='utf-8') as f:
        sys.stderr = f
        try:
            while True:
                try:
                    updater = Updater(f'{TOKEN}', use_context=True)
                    dp = updater.dispatcher
                    dp.add_handler(CommandHandler('start', start))
                    dp.add_handler(CommandHandler('restart', restart))
                    dp.add_handler(CallbackQueryHandler(button))
                    dp.add_handler(MessageHandler(Filters.text, handle_text, run_async=True))
                    updater.start_polling()
                    updater.idle()
                    pass
                except NetworkError:
                    # Обработка ошибки "потеря соединения"
                    print(f'Соединение потеряно. Повторное подключение...')
                    time.sleep(5)
                except Unauthorized:
                    # Обработка ошибки "неавторизованный доступ"
                    print('Ошибка авторизации. Проверьте токен.')
                    break
                except Exception as e:
                    # Общая обработка всех остальных ошибок
                    print(f'Error occurred: {e}')
                    time.sleep(5)
        except Exception as e:
            sys.stderr.write(str(e))


if __name__ == '__main__':
    main()
