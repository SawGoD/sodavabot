import datetime
import json
import os
import re
import socket
import subprocess
import threading
import time

import keyboard
import mss
import psutil
import pyautogui
import pygetwindow as gw
import pyperclip
import screeninfo
import telegram
from dotenv import load_dotenv
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup

import blocks.u_common_func
from blocks import s_path, u_send_logs
from blocks.s_path import (DEFPATH, KILL, SPEAK_HEAD_A, SPEAK_HEAD_H,
                           SPEAK_HEAD_S, SPEAK_MON_L, SPEAK_MON_R, SVCL,
                           dict_of_num, filler)
from blocks.u_common_func import (clock, menu_updater, mod_fix, sound_alert,
                                  thread_make, user_input)
from blocks.u_handle_db import read_db_cell, write_db_cell

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)

s_con_path = "s_connection.json"


def get_volume():
    if read_db_cell("output_device",) == "headphones_h":
        keys = [SPEAK_HEAD_H[1], "head_h"]
    elif read_db_cell("output_device") == "headphones_s":
        keys = [SPEAK_HEAD_S[1], "head_s"]
    elif read_db_cell("output_device") == "headphones_a":
        keys = [SPEAK_HEAD_A[1], "head_a"]
    elif read_db_cell("output_device") == "monitor_r":
        keys = [SPEAK_MON_R[1], "mon_r"]
    elif read_db_cell("output_device") == "monitor_l":
        keys = [SPEAK_MON_L[1], "mon_l"]
    else:
        return

    try:
        vol = int(round(float(subprocess.check_output(
            f"{SVCL} {keys[0]}".split()).decode('utf-8').strip())))
    except ValueError:
        vol = 0
    write_db_cell("volume", vol, keys[1])


def set_output_device(device, query):
    os.system(f'{s_path.SETDEVDEF} {device[0]}')
    os.system(f'{s_path.SETDEVDEFCOMM} {device[0]}')
    device_name = ''
    if read_db_cell("pc", None) == 1:
        device_name = "headphones_h" if device == SPEAK_HEAD_H \
            else "monitor_r" if device == SPEAK_MON_R \
            else "monitor_l" if device == SPEAK_MON_L \
            else "none"
        current_markup = query.message.reply_markup
        current_markup.inline_keyboard[0][
            0].text = f"🌀 {read_db_cell('volume', 'head_h')} {'🟢' if device == SPEAK_HEAD_H else '⚫️'}"
        current_markup.inline_keyboard[0][
            1].text = f"{'🟢' if device == SPEAK_MON_R else '⚫️'} {read_db_cell('volume', 'mon_r')} 🖥"
        current_markup.inline_keyboard[1][
            0].text = f"{'🟢' if device == SPEAK_MON_L else '⚫️'} {read_db_cell('volume', 'mon_l')} 🖥"
        query.edit_message_reply_markup(reply_markup=current_markup)
    elif read_db_cell("pc", None) == 2:
        device_name = "headphones_h" if device == SPEAK_HEAD_H \
            else "headphones_s" if device == SPEAK_HEAD_S \
            else "headphones_a" if device == SPEAK_HEAD_A \
            else "monitor_r" if device == SPEAK_MON_R \
            else "none"
        current_markup = query.message.reply_markup
        current_markup.inline_keyboard[0][
            0].text = f"🌀 {read_db_cell('volume', 'head_h')} {'🟢' if device == SPEAK_HEAD_H else '⚫️'}"
        current_markup.inline_keyboard[0][
            1].text = f"{'🟢' if device == SPEAK_MON_R else '⚫️'} {read_db_cell('volume', 'mon_r')} 🖥"
        current_markup.inline_keyboard[1][
            0].text = f"🎸 {read_db_cell('volume', 'head_s')} {'🟢' if device == SPEAK_HEAD_S else '⚫️'}"
        current_markup.inline_keyboard[1][
            1].text = f"{'🟢' if device == SPEAK_HEAD_A else '⚫️'} {read_db_cell('volume', 'head_a')} 🩸"
        query.edit_message_reply_markup(reply_markup=current_markup)
    write_db_cell("output_device", device_name)


def take_screenshot(key, context, update):
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    if not os.path.exists(s_path.SCREENPATH):
        os.makedirs(s_path.SCREENPATH)
    for file_name in os.listdir(s_path.SCREENPATH):
        file_path = os.path.join(s_path.SCREENPATH, file_name)
        os.remove(file_path)
    if key in range(-1, 9):
        sct = mss.mss()
        file = sct.shot(
            mon=key, output=f'{s_path.SCREENPATH}/screen_{mod_fix(mod_type="name")}.png')
    elif key == None:
        active_window = gw.getActiveWindow()
        x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height
        with mss.mss() as sct:
            monitor = {"left": x, "top": y, "width": width, "height": height}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size,
                             output=f'{s_path.SCREENPATH}/screen_{mod_fix(mod_type="name")}.png')
    for filename in os.listdir(s_path.SCREENPATH):
        photo_message = context.bot.send_photo(chat_id=update.effective_chat.id,
                                               photo=open(os.path.join(
                                                   s_path.SCREENPATH, filename), 'rb'),
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Удалить",
                                                                                                        callback_data=f"scrn_del:{filename}")]]))
        # сохраняем ID сообщения в UserDict
        context.user_data[filename] = photo_message.message_id
    if read_db_cell("sound_status") == 1:
        sound_alert("sound_screenshot.mp3")


def speed_test():
    u_send_logs.log_form_cmd(update=None, context=None,
                             cmd=speed_test.__name__,
                             action="запущен", effect=True)
    while True:
        p = subprocess.Popen(
            fr'"{DEFPATH}\resource\speedtest.exe" --format=json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,  # Перенаправляем stderr в stdout
            shell=True, text=True)
        time.sleep(30)
        result = p.communicate()[0]
        with open(fr'{DEFPATH}\data\s_connection.json', 'w') as f:
            f.write(result)


def time_to_upd(upd_time, cur_time):
    upd_time_obj = datetime.datetime.strptime(upd_time, "%H:%M:%S")
    cur_time_obj = datetime.datetime.strptime(cur_time, "%H:%M:%S")
    time_diff = (upd_time_obj - cur_time_obj).total_seconds()
    if time_diff < 0:
        time_diff += 30
    return int(time_diff)


def explorer_fix():
    os.system(f"{KILL} explorer.exe")
    os.system("start explorer.exe")


def check_health():
    while True:
        if read_db_cell("pc_health_check", "check_status") == 1:
            cpu_percent = psutil.cpu_percent(interval=3)
            write_db_cell("pc_health_check", cpu_percent, "cpu")
            memory = psutil.virtual_memory()
            write_db_cell("pc_health_check", memory.percent, "ram")


def computer_menu(update, context):
    user_input(0, "none")
    write_db_cell("pc_health_check", 0, "check_status")
    write_db_cell("updater_status", 0)
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [[InlineKeyboardButton("🔂 Мультимедиа", callback_data='multi'),
                 InlineKeyboardButton("🔒 VPN", callback_data='vpn')],
                [InlineKeyboardButton("📷 Экран", callback_data='screen'),
                 InlineKeyboardButton("📋 Буфер обмена", callback_data='clipboard')],
                [InlineKeyboardButton("🏃‍♂️ Состояние", callback_data='health'),
                 InlineKeyboardButton("⚠ Питание", callback_data='power')],
                [InlineKeyboardButton(
                    "📊 Дополнительно", callback_data='additional_pc_menu')],
                [InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🖥 *Компьютер*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def multi_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    get_volume()
    keyboard = [
        [InlineKeyboardButton(f"🌀 {read_db_cell('volume', 'head_h')} "
                              f"{'🟢' if read_db_cell('output_device') == 'headphones_h' else '⚫'}",
                              callback_data='set_dev_head_h'),
         InlineKeyboardButton(f"{'🟢' if read_db_cell('output_device') == 'monitor_r' else '⚫'} "
                              f"{read_db_cell('volume', 'mon_r')} 🖥",
                              callback_data='set_dev_mon_r')]]
    if read_db_cell("pc", None) == 1:
        keyboard.append([InlineKeyboardButton(f"{'🟢' if read_db_cell('output_device') == 'monitor_l' else '⚫'} "
                                              f"{read_db_cell('volume', 'mon_l')} 🖥",
                                              callback_data='set_dev_mon_l')])
    elif read_db_cell("pc", None) == 2:
        keyboard.append([InlineKeyboardButton(
            f"🎸 {read_db_cell('volume', 'head_s')} "
            f"{'🟢' if read_db_cell('output_device') == 'headphones_s' else '⚫'}",
            callback_data='set_dev_head_s'),
            InlineKeyboardButton(
                f"{'🟢' if read_db_cell('output_device') == 'headphones_a' else '⚫'} "
                f"{read_db_cell('volume', 'head_a')} 🩸",
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
                 InlineKeyboardButton(f"{'🔇' if read_db_cell('volume_status') == 0 else '🔊'}",
                                      callback_data='vol_on_off'),
                 InlineKeyboardButton("+10", callback_data="vol_up10"),
                 InlineKeyboardButton("➕", callback_data='vol_up')]]

    if read_db_cell("hints_status") == 1:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("💡", callback_data='hints_multi'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    else:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🔂 *Мультимедиа*{mod_fix()}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def vpn_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    daten, timen = clock()
    try:
        download = ((read_db_cell("download", 'bytes', filename=s_con_path) * 8) /
                    (read_db_cell("download", 'elapsed', filename=s_con_path) * 1000))
        upload = ((read_db_cell("upload", 'bytes', filename=s_con_path) * 8) /
                  (read_db_cell("upload", 'elapsed', filename=s_con_path) * 1000))
        sp_avg = round((download + upload) / 2, 2)

        url = read_db_cell("result", 'url', filename=s_con_path)
        ping = round(read_db_cell("ping", 'latency', filename=s_con_path), 2)
        int_ip = read_db_cell("interface", 'internalIp', filename=s_con_path)
        ext_ip = read_db_cell("interface", 'externalIp', filename=s_con_path)
        upd_time = read_db_cell("timestamp", filename=s_con_path)[11:-1]
        upd_time = timen[:-6] + upd_time[2:]
        left_time = str(time_to_upd(
            str(upd_time), str(timen))).replace('-', '')
    except (json.decoder.JSONDecodeError, KeyError, FileNotFoundError, ValueError) as err:
        int_ip = socket.gethostbyname(socket.gethostname())
        ping, ext_ip = "0", "0.0.0.0"
        sp_avg = "0.00"
        url, upd_time, left_time = "", timen, "0"

    about = fr'''[Данные сети]({url}):
            _Задержка:_ `{ping}ms`
            _Внутренний IP:_ `{int_ip}`
            _Внешний IP:_ `{ext_ip}`
\- \- \- \- \- \- \- \- \- \- \- \- \- \- \- \-
    _Обновлено:_ {upd_time}
    _Осталось:_ {left_time}сек'''
    keyboard = [[InlineKeyboardButton(f"🇩🇪 DE-tcp {'🟢' if read_db_cell('vpn_status') == 'vpn_1' else '⚫'}",
                                      callback_data='vpn_1'),
                 InlineKeyboardButton(f"🇹🇷 TR-tcp {'🟢' if read_db_cell('vpn_status') == 'vpn_2' else '⚫'}",
                                      callback_data='vpn_2'),
                 InlineKeyboardButton(f"🇱🇹 LT-tcp {'🟢' if read_db_cell('vpn_status') == 'vpn_3' else '⚫'}",
                                      callback_data='vpn_3')],
                [InlineKeyboardButton(f"🇩🇪 DE-udp {'🟢' if read_db_cell('vpn_status') == 'vpn_4' else '⚫'}",
                                      callback_data='vpn_4'),
                 InlineKeyboardButton(f"🇺🇦 UA-udp {'🟢' if read_db_cell('vpn_status') == 'vpn_5' else '⚫'}",
                                      callback_data='vpn_5'),
                 InlineKeyboardButton(f"🇫🇮 FI-udp {'🟢' if read_db_cell('vpn_status') == 'vpn_6' else '⚫'}",
                                      callback_data='vpn_6')],

                [InlineKeyboardButton(f"📶 Mbps: {sp_avg}", callback_data='con_speed'),
                 InlineKeyboardButton("⭕ Выключить ", callback_data='vpn_off')],

                [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🔒 *VPN*{mod_fix()}\n{about}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
    if read_db_cell("updater_status") == 0:
        write_db_cell("updater_status", 1)
        thread_make("updater_speed", menu_updater, vpn_menu, update, context)


def power_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [
        # [InlineKeyboardButton(f"⚫🟢 Состояние LED [x] ", callback_data='led_upd')],
        [InlineKeyboardButton("🔄", callback_data='pc_reb'),
         InlineKeyboardButton("💤", callback_data='pc_hyb'),
         InlineKeyboardButton("⭕", callback_data='pc_off')],
        [InlineKeyboardButton("🚫 Отмена", callback_data='pc_canc')],
        [InlineKeyboardButton("🙈", callback_data='mon_off')]]

    if read_db_cell("hints_status") == 1:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("💡", callback_data='hints_power'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    else:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}⚠ *Питание*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def screen_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    num_monitors = len(screeninfo.get_monitors())
    keyboard = [
        [InlineKeyboardButton("🔳", callback_data='scrn_full')]]
    keyboard_add = []
    for i in range(1, num_monitors + 1):
        keyboard_add.append(InlineKeyboardButton(f"{dict_of_num[i]}", callback_data=f'scrn_{i}'))
    keyboard.append(keyboard_add)
    keyboard.append([InlineKeyboardButton("◾", callback_data='scrn_app')])

    if read_db_cell("hints_status") == 1:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton(
                            "💡", callback_data='hints_screen'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    else:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}📷 *Экран*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


def clipboard_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    link = None
    if pyperclip.paste():
        mes = pyperclip.paste()
        if len(mes) > 4030:
            mes = mes[:4030]
        if re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', mes):
            link = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', mes)[0]
            link = re.sub(r'[\]\),\']', '', link)
    else:
        mes = "Пусто"
    mes = mes.replace('{', '\{').replace('}', '\}')
    keyboard = [
        [InlineKeyboardButton("🗑️ Очистить", callback_data='clear_clipboard')]]
    if link is not None:
        keyboard.append([InlineKeyboardButton("🔗 Ссылка", url=link)])
    if read_db_cell("hints_status") == 1:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton(
                            "💡", callback_data='hints_clipboard_menu'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    else:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}📋 *Буфер обмена*{mod_fix()}\n`{mes}`",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
    if read_db_cell("updater_status") == 0:
        write_db_cell("updater_status", 1)
        thread_make("updater_speed", menu_updater,
                    clipboard_menu, update, context)


def health_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    write_db_cell("pc_health_check", 1, "check_status")
    mes = f'''
CPU: {read_db_cell("pc_health_check", "cpu")}%
RAM: {read_db_cell("pc_health_check", "ram")}%
    '''
    mes = mes.replace(".", r"\.")
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🏃‍♂️ *Состояние*{mod_fix()}{mes}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
    if read_db_cell("updater_status") == 0:
        write_db_cell("updater_status", 1)
        thread_make("updater_health", menu_updater,
                    health_menu, update, context)


def additional_pc_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    keyboard = [
        [InlineKeyboardButton("🗂️ Перезапуск", callback_data='explorer_fix')]]
    if read_db_cell("hints_status") == 1:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton(
                            "💡", callback_data='hints_additional_pc_menu'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    else:
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                        InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}📊 *Дополнительно*",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)


thread_speed_test = threading.Thread(target=speed_test)
thread_check_health = threading.Thread(target=check_health)
