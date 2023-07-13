import time
import datetime
import threading
import subprocess
# import concurrent.futures
import winreg
import json
import os
# 2023      Март, апрель, май, июнь
start_date = 1 + 1 + 1 + 1 + 1

ver = str(f'{start_date}.13b')

NOW = datetime.datetime.now()
now_date = NOW.strftime("%d.%m.%y")
now_time = NOW.strftime('%H:%M:%S')


def create_main_db():
    filepath = ".\\data\\s_main_db.json"
    if not os.path.exists(filepath):
        data = {
            "users": [
                "334969852",
                "6285956805",
                "473352655"
            ],
            "log_output": "-1001891369938",
            "pc": 2,
            "cur_pc": "👩🏻‍💻 Домашний ПК",
            "volume_status": 1,
            "output_device": "",
            "volume": {
                "head_h": 0,
                "head_s": 0,
                "head_a": 0,
                "mon_r": 0,
                "mon_l": 0
            },
            "app_name": "",
            "waiting_input": 0,
            "handle_type": "none",
            "vpn_status": "off",
            "sd_link_local": "",
            "sd_link_share": "",
            "sdai_status": ""
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            # f.seek(0)
            # f.truncate()


create_main_db()
time.sleep(0.15)


def read_db_cell(cell, subcell=None, filename='s_main_db.json'):
    filepath = os.path.join('.', 'data', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if subcell is None:
            return data[cell]
        else:
            return data[cell][subcell]
        # read_db_cell("cell", "subcell"/None, "filename")


def write_db_cell(cell, value, subcell=None, filename="s_main_db.json"):
    with open(f'data/{filename}', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        if subcell is None:
            data[cell] = value
        else:
            data[cell][subcell] = value
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()
        # write_db_cell("cell", значение, "subcell", "filename")


def clear_db(filename='s_main_db.json'):
    filepath = os.path.join('.', 'data', filename)
    with open(filepath, 'w') as f:
        json.dump({}, f)


def get_path(path, file):
    # Открываем ключ реестра, содержащий информацию о приложении Steam
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        fr"Software\{path}")
    value, reg_type = winreg.QueryValueEx(key, file)
    # Возвращаем найденный путь
    return value


def user_input(s, h_type):
    write_db_cell("waiting_input", s)
    write_db_cell("handle_type", h_type)


if read_db_cell("pc") == 1:     # Рабочий ПК
    # BROWSER = "C:/Users/karelikov/AppData/Local/Programs/Opera/launcher.exe"
    # STEAM = r'C:/Program Files (x86)/Steam'
    SPEAK_HEAD_H = "Наушники (HONOR Magic Earbuds Stereo)", \
        "{0.0.0.00000000}.{03e928b3-a42f-4a88-b7e5-f3c66adb1f11}"
    SPEAK_MON_R = "Динамики (2- High Definition Audio Device)",\
        "{0.0.0.00000000}.{69f9cfe0-7cb7-4517-96ed-a816a26655f3}"
    SPEAK_MON_L = "BenQ EW2775ZH (Аудио Intel(R) для дисплеев)",\
        "{0.0.0.00000000}.{129de811-bfb3-4a98-96d3-0867c3ab5906}"
elif read_db_cell("pc") == 2:   # Домашний ПК
    # BROWSER = "A:/Browsers/launcher.exe"
    # STEAM = r'G:/Steam'
    SPEAK_HEAD_H = "Наушники (HONOR Magic Earbuds)", \
        "{0.0.0.00000000}.{5f0d3099-ef36-4600-af3a-ea4f1886dedd}"
    SPEAK_HEAD_S = "Headset (2- SB Tactic3D Rage Wireless)",\
        "{0.0.0.00000000}.{93389548-8b7a-48a2-bd56-7c3ac4101744}"
    SPEAK_HEAD_A = "Bloody G575 (3- USB Audio Device)", \
        "{0.0.0.00000000}.{32aae43c-1c38-4d36-823a-785fdea69a6c}"
    SPEAK_MON_R = "DELL S2316H (NVIDIA High Definition Audio)",\
        "{0.0.0.00000000}.{1a6e09ed-9668-41da-b347-a5ce8fb88003}"


fizz = "o_r"
glee = "4"
jolt = "hal"
yank = "0z"
hush = "_me"

DEFPATH = r'C:\Soda_VA_BOT'

# Путь для исполнения
BROWSER = get_path(r'Opera Software', 'Last Stable Install Path')+'launcher.exe'
STEAM = get_path(r'Valve\Steam', 'SteamPath')
VPN_PATH = get_path(r'Microsoft\Windows\CurrentVersion\Run', 'OpenVPN-GUI')
STEAMCMD = fr'{STEAM}\steamcmd.exe'
INCOGNITO = f'"{BROWSER}" --private'
NIRCMD = fr'{DEFPATH}/resource/nircmd.exe'

SHAREX = fr'{DEFPATH}\resource\ShareX\full_screen'

DE = 'DE-Frankfurt.ovpn'
TR = 'TR-Istanbul.ovpn'
LT = 'LT-Vilnius.ovpn'

VPN_ON = fr'"{VPN_PATH}" --connect LT-Vilnius.ovpn'
VPN_TO = fr'"{VPN_PATH}" --connect'
VPN_OFF = fr'"{VPN_PATH}" --command disconnect_all'
SVCL = fr"{DEFPATH}\resource\svcl.exe /Stdout /GetPercent"
SETVOL = fr"{DEFPATH}\resource\SetVol.exe"
SETDEVDEF = fr'"{DEFPATH}\resource\SetVol.exe" makedefault device'
SETDEVDEFCOMM = fr'"{DEFPATH}\resource\SetVol.exe" makedefaultcomm device'
YARU = "https://yandex.ru/search/touch/?text="
KILLOP = "TASKKILL /F /IM opera.exe"
KILL = "TASKKILL /F /IM"

menu_buttons = {
    'computer': 'computer_menu(update, context)',
    'apps': 'app_menu(update, context)',

    'about_bot': 'about_text(update, context)',

    'multi': 'multi_menu(update, context)',
    'pc': 'pc_menu(update, context)',
    'clipboard': 'clipboard_menu(update, context)',
    'screen': 'screen_menu(update, context)',

    'op_tabs': 'tabs_menu(update, context)',

    'vpn': 'vpn_menu(update, context)',
    'sdai_link': 'sdai_links_menu(update, context)',
    'st_games': 'games_menu(update, context)',

    'script': 'scripts_menu(update, context)',
    'scr_eft': 'scr_eft_menu(update, context)',
}

dict_text_cmd = {
    'pc_off': {'text': 'Компьютер выключится через 15 секунд', 'cmd': 'shutdown /s /t 15'},
    'pc_reb': {'text': 'Компьютер перезагрузится через 15 секунд', 'cmd': 'shutdown /r /t 15'},
    'pc_hyb': {'text': 'Компьютер засыпает', 'cmd': 'shutdown /h'},
    'pc_canc': {'text': 'Выключение компьютера отменено', 'cmd': 'shutdown -a'},
    'mon_off': {'text': 'Мониторы выключены', 'cmd': f'{NIRCMD} monitor async_off'},
    'game_canc': {'text': 'Скачивание игры отменено', 'cmd': f'{KILL} steamcmd.exe'}
}

dict_text_cell = {
    'get_paste': {'text': 'Отправьте текст для копирования( 4096 ):', 'cell': 'clipboard'},
    'tab_send': {'text': 'Отправьте ссылку:', 'cell': 'links'},
    'game_send': {'text': 'Введите: Game 2FA', 'cell': 'game'},
}

app_data = {
    'opera': {
        'app_on': 'op_on',
        'app_off': 'op_off',
        'app_sub': 'op_tabs',
        'app_sub_text': '📑 Вкладки',
        'app_ui_name': '🌐 *Opera*'
    },
    'steam': {
        'app_on': 'st_on',
        'app_off': 'st_off',
        'app_sub': 'st_games',
        'app_sub_text': '📑 Игры',
        'app_ui_name': '🕹️ *Steam*'
    },
    'sdai': {
        'app_on': 'sdai_on',
        'app_off': 'sdai_off',
        'app_sub': 'sdai_link',
        'app_sub_text': '🔗 Ссылки',
        'app_ui_name': '🎨️ *Stable Diffusion*'
    }
}

apps_os_act = {
    # Opera
    'op_on': BROWSER,
    'opi_on': INCOGNITO,
    'op_off': f'{KILL} opera.exe',

    # SDAI
    'sdai_on': 'start "SDAI Monitor" S:/SD/webui-user.bat',
    'sdai_off': '',

    # Steam
    'st_off': f'{STEAM}/steam.exe'

}

multi_act = {
    'set_dev_head_h': 'set_output_device(s_path.SPEAK_HEAD_H, query)',
    'set_dev_head_s': 'set_output_device(s_path.SPEAK_HEAD_S, query)',
    'set_dev_head_a': 'set_output_device(s_path.SPEAK_HEAD_A, query)',
    'set_dev_mon_r': 'set_output_device(s_path.SPEAK_MON_R, query)',
    'set_dev_mon_l': 'set_output_device(s_path.SPEAK_MON_L, query)',
    'multi_pull': 'pyautogui.press("left")',
    'multi_force': 'pyautogui.press("right")',
    'multi_on_off': 'pyautogui.press("playpause")',
    'multi_next': 'pyautogui.press("nexttrack")',
    'multi_prev': 'pyautogui.press("prevtrack")',
}

scr_keys = {
    'scrn_full': 'ctrl',
    'scrn_mon': 'alt',
    'scrn_app': 'shift'
}


vpn_paths = {
    'vpn_1': DE,
    'vpn_2': TR,
    'vpn_3': LT
}

tabs_hotkeys = {
    'tab_pull': ('ctrl', 'pgup'),
    'tab_force': ('ctrl', 'pgdn'),
    'tab_prev': ('alt', 'left'),
    'tab_next': ('alt', 'right'),
    'tab_off': ('ctrl', 'w'),
    'tab_return': ('ctrl', 'shift', 't')
}


def ver_greet():
    for i in range(1):
        print('')
    print("==================")
    print(f"Soda v{ver} started")
    print("Дата:", now_date)
    print("Время:", now_time)
    print("==================")
    print(f'Компьютер: {read_db_cell("cur_pc")}')


filler = '==================================\n'


def get_volume():
    if read_db_cell("output_device", None) == "headphones_h":
        keys = [SPEAK_HEAD_H[1], "head_h"]
    elif read_db_cell("output_device", None) == "headphones_s":
        keys = [SPEAK_HEAD_S[1], "head_s"]
    elif read_db_cell("output_device", None) == "headphones_a":
        keys = [SPEAK_HEAD_A[1], "head_a"]
    elif read_db_cell("output_device", None) == "monitor_r":
        keys = [SPEAK_MON_R[1], "mon_r"]
    elif read_db_cell("output_device", None) == "monitor_l":
        keys = [SPEAK_MON_L[1], "mon_l"]
    else:
        return

    try:
        vol = int(round(float(subprocess.check_output(f"{SVCL} {keys[0]}".split()).decode('utf-8').strip())))
    except ValueError:
        vol = 0
    write_db_cell("volume", vol, keys[1])


# def get_volume():
#     if read_db_cell("pc", None) == 1:
#         commands = [(SPEAK_HEAD_H[1], "head_h"), (SPEAK_MON_R[1], "mon_r"),
#                     (SPEAK_MON_L[1], "mon_l")]
#     elif read_db_cell("pc", None) == 2:
#         commands = [(SPEAK_HEAD_H[1], "head_h"), (SPEAK_HEAD_S[1], "head_s"),
#                     (SPEAK_HEAD_A[1], "head_a"), (SPEAK_MON_R[1], "mon_r")]
#     else:
#         return
#
#     for cmd, key in commands:
#         try:
#             vol = int(round(float(subprocess.check_output(f"{SVCL} {cmd}".split()).decode('utf-8').strip())))
#         except ValueError:
#             vol = 0
#         write_db_cell("volume", vol, key)


def speed_test():
    print("Модуль измерения скорости запущен.")
    while True:
        p = subprocess.Popen(fr'"{DEFPATH}\resource\speedtest.exe" --format=json', stdout=subprocess.PIPE, shell=True, text=True)
        # Ждем 30 секунд до окончания проверки
        time.sleep(30)
        # Получаем результат выполнения команды
        result = p.communicate()[0]
        # Сохраняем результат в файл
        with open(fr'{DEFPATH}\data\s_connection.json', 'w') as f:
            f.write(result)


thread_speed_test = threading.Thread(target=speed_test)
true_try = jolt+fizz+yank+glee+hush
