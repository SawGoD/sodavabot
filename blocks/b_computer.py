import datetime
import json
import os
import re
import socket
import subprocess
import threading
import time
import shutil
import string

import keyboard
import mss
import psutil
import pyautogui
import pygetwindow as gw
import pyperclip
import screeninfo
import telegram

import pycaw.pycaw as pycaw # ! новая библиотека pycaw
import win32gui # ! новая библиотека pywin32
from ctypes import cast, POINTER
import comtypes
from comtypes import CLSCTX_ALL # ! новая библиотека comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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
    try:
        comtypes.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume.GetMasterVolumeLevelScalar() * 100
        vol = f"{current_volume:.0f}"
    except:
        vol = 0
        
    write_db_cell("volume", vol, read_db_cell("output_device"))


def set_output_device(device, query):
    os.system(f'{s_path.SETDEVDEF} {device}')
    os.system(f'{s_path.SETDEVDEFCOMM} {device}')
    device_name = "headphones_h" if device == SPEAK_HEAD_H \
            else "headphones_s" if device == SPEAK_HEAD_S \
            else "headphones_a" if device == SPEAK_HEAD_A \
            else "monitor_r" if device == SPEAK_MON_R \
            else "none"
    current_markup = query.message.reply_markup
    current_markup.inline_keyboard[0][
        0].text = f"🌀 {read_db_cell('volume', 'headphones_h')} {'🟢' if device == SPEAK_HEAD_H else '⚫️'}"
    current_markup.inline_keyboard[0][
        1].text = f"{'🟢' if device == SPEAK_MON_R else '⚫️'} {read_db_cell('volume', 'monitor_r')} 🖥"
    current_markup.inline_keyboard[1][
        0].text = f"🎸 {read_db_cell('volume', 'headphones_s')} {'🟢' if device == SPEAK_HEAD_S else '⚫️'}"
    current_markup.inline_keyboard[1][
        1].text = f"{'🟢' if device == SPEAK_HEAD_A else '⚫️'} {read_db_cell('volume', 'headphones_a')} 🩸"
    query.edit_message_reply_markup(reply_markup=current_markup)
    write_db_cell("output_device", device_name)


def take_screenshot(key, context, update):
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    title = None if title == "" else f"*Активное окно*: `{title}`"

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
                                               caption=title,  # Добавлен заголовок к фото
                                               parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Удалить",
                                                                                                        callback_data=f"scrn_del:{filename}")]]))
        # сохраняем ID сообщения в UserDict
        context.user_data[filename] = photo_message.message_id
    if read_db_cell("sound_status") == 1:
        sound_alert("sound_screenshot.mp3")


def speed_test():
    if read_db_cell("speedtest_status") == 1:
        u_send_logs.log_form_cmd(update=None, context=None,
                                cmd=speed_test.__name__,
                                action="запущен", effect=True)
    elif read_db_cell("speedtest_status") == 0:
        u_send_logs.log_form_cmd(update=None, context=None,
                                cmd=speed_test.__name__,
                                action="запущен", effect=False)
    while True:
        if read_db_cell("speedtest_status") == 1:
            p = subprocess.Popen(
                fr'"{DEFPATH}\resource\speedtest.exe" --format=json',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,  # Перенаправляем stderr в stdout
                shell=True, text=True)
            time.sleep(30)
            result = p.communicate()[0]
            with open(fr'{DEFPATH}\data\s_connection.json', 'w') as f:
                f.write(result)
        elif read_db_cell("speedtest_status") == 0:
            try:
                os.system("taskkill /F /IM speedtest.exe > nul 2>&1")
            except Exception as e:
                pass


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
            

def check_memory(disk_symbol=None):
    if disk_symbol is None:
        disk_info = ""
        for letter in string.ascii_uppercase:
            try:
                total, used, free = shutil.disk_usage(f"{letter}:\\")
                total_gb = total / (1024**3)
                used_gb = used / (1024**3)
                free_gb = free / (1024**3)
                disk_info += f"*Диск {letter}*: `{used_gb:.2f}` ГБ / `{total_gb:.2f}` ГБ\n"
            except FileNotFoundError:
                pass
        return disk_info
    else:
        try:
            total, used, free = shutil.disk_usage(f"{disk_symbol.upper()}:\\")
            used_mem = used / (total / 100)
            disk_info = f"{used_mem:.2f}"
        except FileNotFoundError:
            disk_info = f"0"
        return disk_info
    

def memory_stats(clear_flag=False):

    temp_files_paths = {
        'appdata_temp_path': os.path.expanduser('~') + "\\AppData\\Local\\Temp",
        'win_temp_path': os.path.join("C:\Windows\Temp"),
        'recycle_bin_path': os.path.join("C:\$Recycle.bin"),
    }
    
    if not clear_flag:
        total_size = 0

        for path_key, path_value in temp_files_paths.items():
            for dirpath, dirnames, filenames in os.walk(path_value):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)

        total_size_gb = total_size / (1024**3)  # переводим размер в гигабайты
        return f"{total_size_gb:.2f}"
    elif clear_flag:
        for path_key, path_value in temp_files_paths.items():
            for dirpath, dirnames, filenames in os.walk(path_value):
                for item in dirnames + filenames:
                    item_path = os.path.join(dirpath, item)
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    except:
                        pass

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
        [InlineKeyboardButton(f"🌀 {read_db_cell('volume', 'headphones_h')} "
                              f"{'🟢' if read_db_cell('output_device') == 'headphones_h' else '⚫'}",
                              callback_data='set_dev_head_h'),
         InlineKeyboardButton(f"{'🟢' if read_db_cell('output_device') == 'monitor_r' else '⚫'} "
                              f"{read_db_cell('volume', 'monitor_r')} 🖥",
                              callback_data='set_dev_mon_r')]]

    keyboard.append([InlineKeyboardButton(
        f"🎸 {read_db_cell('volume', 'headphones_s')} "
        f"{'🟢' if read_db_cell('output_device') == 'headphones_s' else '⚫'}",
        callback_data='set_dev_head_s'),
        InlineKeyboardButton(
            f"{'🟢' if read_db_cell('output_device') == 'headphones_a' else '⚫'} "
            f"{read_db_cell('volume', 'headphones_a')} 🩸",
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
    mes = mes.replace('{', '\{').replace('}', '\}').replace('\\', r"\\")
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
    cpu = read_db_cell("pc_health_check", "cpu")
    ram = read_db_cell("pc_health_check", "ram")
    disk_c = check_memory("C")
    
    cpu_str = f"*CPU*: `{cpu}`%".ljust(17, ' ')
    disk_c_str = f"*Диск C*: `{disk_c}`%".center(17, ' ')
    ram_str = f"*RAM*: `{ram}`%".rjust(17, ' ')
    
    mes = f"\n{cpu_str}{disk_c_str}{ram_str}"
    mes = mes.replace(".", r"\.")
    keyboard = [[InlineKeyboardButton("💾 Память", callback_data='memory')],
                [InlineKeyboardButton("🔙 Назад", callback_data='computer'),
                 InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}🏃‍♂️ *Состояние*{mod_fix()}{mes}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
    if read_db_cell("updater_status") == 0:
        write_db_cell("updater_status", 1)
        thread_make("updater_health", menu_updater,
                    health_menu, update, context)
        

def memory_menu(update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)
    write_db_cell("pc_health_check", 0, "check_status")
    write_db_cell("updater_status", 0)
    mes = f'''{check_memory()}'''
    mes = mes.replace(".", r"\.")
    keyboard = []
    keyboard_add = []
    if float(memory_stats()) > 0.8:
        keyboard = [[InlineKeyboardButton(f"🗑️ Очистить (C:) {memory_stats()} ГБ", callback_data='clear_memory')],
            [InlineKeyboardButton("🔙 Назад", callback_data='health'),
            InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    else:
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='health'),
            InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
        
        
    # if read_db_cell("hints_status") == 1:
    #     keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='health'),
    #                     InlineKeyboardButton(
    #                         "💡", callback_data='hints_memory'),
    #                     InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
    # else:
    #     keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='health'),
                        # InlineKeyboardButton("🔝 Меню", callback_data='mmenu')])
        
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}💾 *Память*{mod_fix()}\n{mes}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
    


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
