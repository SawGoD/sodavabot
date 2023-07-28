import re
import os
import sys
import pyperclip
import requests
import subprocess
import pyautogui
import telegram
from dotenv import load_dotenv
from blocks import u_send_logs
from blocks import s_path
from blocks.b_computer import computer_menu, multi_menu, vpn_menu, power_menu, screen_menu, clipboard_menu, \
    take_screenshot
from blocks.b_app import app_menu, app_ui, tabs_menu, scripts_menu, scr_eft_menu, games_menu, sdai_links_menu
from blocks.b_about import bot_about, bot_changes, bot_settings, update_menu_range
from blocks.u_common_func import sound_alert, user_input
from blocks.s_scripts_list import sdb_path
from blocks.u_handle_db import read_db_cell, write_db_cell
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction


user_data = {}
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)


def handle_text(update, context):
    message_text = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    user_id = str(update.message.chat_id)
    if user_id not in os.getenv('ALLOWED_USERS'):
        context.bot.send_message(chat_id=user_id, text="У Вас нет доступа")
        u_send_logs.log_form_cmd(update, context, effect=False, cmd="handle_text")
        u_send_logs.log_form_tg(update, context, effect=False, cmd="handle_text")
    else:
        u_send_logs.log_form_cmd(update, context, effect=True, cmd="handle_text")
        u_send_logs.log_form_tg(update, context, effect=True, cmd="handle_text")
        if read_db_cell("waiting_input") == 1:
            if read_db_cell("handle_type") == 'links':
                urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', message_text)
                message_text = urls[0]
                os.system(f'{s_path.BROWSER} "{message_text}"')
            elif read_db_cell("handle_type") == 'clipboard':
                pyperclip.copy(message_text)
            elif read_db_cell("handle_type") == 'game':
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

                game_name = message_text[:-6]
                code_2fa = message_text[-5:]
                appid = get_appid(game_name)
                if appid:
                    print(f"AppID игры {game_name}: {appid}")
                    install_dir = fr'{s_path.STEAM}/steamapps/common/'
                    cmd = f'"{s_path.STEAMCMD}" +force_install_dir {install_dir}' \
                          f' +login {str(os.getenv("STEAM_LOGIN"))} {str(os.getenv("STEAM_PASS"))} {str(code_2fa)} ' \
                          f'+app_update {str(appid)} validate +quit'
                    # lets_install = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    os.system(cmd)
                else:
                    print(f"Игра {game_name} не найдена")
        else:
            pyperclip.copy(message_text)
        if read_db_cell("sound_status") == 1:
            sound_alert("sound_text_in.mp3")


def button(update, context):
    query = update.callback_query
    # user = update.effective_user
    user_id = str(query.message.chat_id)
    if user_id not in os.getenv('ALLOWED_USERS'):
        u_send_logs.log_form_tg(update, context, effect=False, alert=os.getenv('LOG_ALERT'))
        u_send_logs.log_form_cmd(update, context, effect=False)
        query.answer(text='У Вас нет доступа')
        pass
    else:
        u_send_logs.log_form_tg(update, context, effect=True, alert=os.getenv('LOG_ALERT'))
        u_send_logs.log_form_cmd(update, context, effect=True)
        if query.data in s_path.menu_buttons:
            eval(s_path.menu_buttons[query.data])
        elif query.data in s_path.multi_act:
            eval(s_path.multi_act[query.data])
        elif query.data in s_path.apps_os_act:
            os.system(s_path.apps_os_act[query.data])
        elif query.data in s_path.tabs_hotkeys:
            pyautogui.hotkey(*s_path.tabs_hotkeys[query.data])
        elif query.data in s_path.scr_keys:
            option = s_path.scr_keys[query.data]
            take_screenshot(option, context, update)
        elif query.data in s_path.dict_text_cmd:
            command = s_path.dict_text_cmd[query.data]
            query.answer(text=command['text'])
            if read_db_cell("sound_status") == 1:
                if query.data in {'pc_off', 'pc_reb'}:
                    sound_alert("sound_shutdown.mp3")
            os.system(command['cmd'])

        elif query.data in s_path.dict_text_cell:
            command = s_path.dict_text_cell[query.data]
            query.answer(text=command['text'])
            user_input(1, command['cell'])

        elif query.data in s_path.vpn_paths:
            query.answer(text='Подключение через 5 секунд')
            os.system(f'{s_path.VPN_TO} {s_path.vpn_paths[query.data]}')
            if query.data == 'vpn_1':
                write_db_cell("vpn_status", "DE")
            elif query.data == 'vpn_2':
                write_db_cell("vpn_status", "TR")
            elif query.data == 'vpn_3':
                write_db_cell("vpn_status", "LT")
            vpn_menu(update, context)

        elif query.data == 'vol_down10':
            query.answer(text='Громкость уменьшена на 10')
            for _ in range(5):
                pyautogui.press("volumedown")
            multi_menu(update, context)
        elif query.data == 'vol_50':
            query.answer(text='Громкость: 50%')
            os.system(fr'"{s_path.SETVOL}" 50')
            multi_menu(update, context)
        elif query.data == 'vol_up10':
            query.answer(text='Громкость увеличена на 10')
            for _ in range(5):
                pyautogui.press("volumeup")
            multi_menu(update, context)
        elif query.data == 'vol_up':
            query.answer(text='Громкость увеличена на 2')
            pyautogui.press("volumeup")
            multi_menu(update, context)
        elif query.data == 'vol_down':
            query.answer(text='Громкость уменьшена на 2')
            pyautogui.press("volumedown")
            multi_menu(update, context)
        elif query.data == 'vol_on_off':
            new_status = 0 if read_db_cell("volume_status") == 1 else 1
            write_db_cell("volume_status", new_status)
            current_markup = query.message.reply_markup
            if new_status == 0:
                current_markup.inline_keyboard[4][2].text = f"🔇"
                # Действие по выключению звука
                pyautogui.press("volumemute")
            else:
                current_markup.inline_keyboard[4][2].text = f"🔊"
                pyautogui.press("volumemute")
            query.edit_message_reply_markup(reply_markup=current_markup)
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
        elif query.data == 'vpn_off':
            query.answer(text='Отключение через 3 секунды')
            os.system(f'{s_path.VPN_OFF}')
            write_db_cell("vpn_status", "off")
            vpn_menu(update, context)

        elif query.data in ['opera', 'steam', 'sdai']:
            write_db_cell("app_name", query.data, None)
            app_ui(update, context)
        elif query.data == 'st_on':
            subprocess.Popen(f'{s_path.STEAM}/steam.exe')

        elif query.data == 'sdai_off':
            # os.system('taskkill /f /PID 8989898')
            print("off - ne rabotaer")

        elif query.data == 'scr_eft_1':
            status = 0 if read_db_cell("script_eft_1", None, filename=sdb_path) == 1 else 1
            write_db_cell(f"script_eft_1", status, None, filename=sdb_path)
            scr_eft_menu(update, context)
        elif query.data == 'eft_1_down':
            x = read_db_cell("seft_1_set", 'value', filename=sdb_path)
            y = x - 1
            write_db_cell("seft_1_set", y, "value", filename=sdb_path)
            scr_eft_menu(update, context)
        elif query.data == "eft_1_5":
            write_db_cell("seft_1_set", 5, "value", filename=sdb_path)
            scr_eft_menu(update, context)
        elif query.data == 'eft_1_up':
            x = read_db_cell("seft_1_set", 'value', filename=sdb_path)
            y = x + 1
            write_db_cell("seft_1_set", y, "value", filename=sdb_path)
            scr_eft_menu(update, context)
        elif query.data == 'scr_eft_2':
            status = 0 if read_db_cell("script_eft_2", None, filename=sdb_path) == 1 else 1
            write_db_cell(f"script_eft_2", status, None, filename=sdb_path)
            scr_eft_menu(update, context)
        elif query.data == 'scr_eft_3':
            status = 0 if read_db_cell("script_eft_3", None, filename=sdb_path) == 1 else 1
            write_db_cell(f"script_eft_3", status, None, filename=sdb_path)
            scr_eft_menu(update, context)
        elif query.data == 'scr_eft_off':
            for i in range(1, 4):
                write_db_cell(f"script_eft_{i}", 0, filename=sdb_path)
            scr_eft_menu(update, context)

        elif query.data == 'sel_pc_1':
            write_db_cell("pc", 1)
            write_db_cell("cur_pc", "👨🏻‍💻 Рабочий ПК")
            query.answer(text='Принудительный перезапуск')
            bot_about(update, context)
            python = sys.executable
            os.execv(python, [python, fr".\soda_va_bot.py"])
        elif query.data == 'sel_pc_2':
            write_db_cell("pc", 2)
            write_db_cell("cur_pc", "👩🏻‍💻 Домашний ПК")
            query.answer(text='Принудительный перезапуск')
            bot_about(update, context)
            python = sys.executable
            os.execv(python, [python, fr".\soda_va_bot.py"])
        elif query.data == 'logger':
            status = 0 if read_db_cell("log_status") == 1 else 1
            write_db_cell(f"log_status", status)
            bot_settings(update, context)
        elif query.data == 'sounds':
            status = 0 if read_db_cell("sound_status") == 1 else 1
            write_db_cell(f"sound_status", status)
            bot_settings(update, context)
        elif query.data == 'bot_changes':
            update_menu_range(update, context, 0, 5, 1)
        elif query.data == 'bot_changes_right':
            update_menu_range(update, context, read_db_cell('menu_range', 'min') + 5,
                              read_db_cell('menu_range', 'max') + 5, read_db_cell('menu_range', 'page') + 1)
        elif query.data == 'bot_changes_left':
            update_menu_range(update, context, read_db_cell('menu_range', 'min') - 5,
                              read_db_cell('menu_range', 'max') - 5, read_db_cell('menu_range', 'page') - 1)
        elif query.data == 'mmenu':
            user_input(0, "none")
            keyboard = [[InlineKeyboardButton("🖥 Компьютер", callback_data='computer')],
                        [InlineKeyboardButton("📟 Приложения", callback_data='apps')],
                        [InlineKeyboardButton("🤖 О боте", callback_data='bot_about')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.edit_message_text(chat_id=user_id, message_id=query.message.message_id,
                                          text=f'{s_path.filler}🔝 *Меню*',
                                          reply_markup=reply_markup,
                                          parse_mode=telegram.ParseMode.MARKDOWN)
