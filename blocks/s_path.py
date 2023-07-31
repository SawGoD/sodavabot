import time
from blocks import s_file_gen
from blocks.u_handle_db import read_db_cell
from blocks.u_common_func import get_path

s_file_gen.create_main_db()
s_file_gen.crete_env()
time.sleep(0.15)


SPEAK_MON_L, SPEAK_MON_R, SPEAK_HEAD_S, SPEAK_HEAD_A, SPEAK_HEAD_H = "", "", "", "", ""

if read_db_cell("pc") == 1:     # Рабочий ПК
    SPEAK_HEAD_H = "Наушники (HONOR Magic Earbuds Stereo)", \
        "{0.0.0.00000000}.{03e928b3-a42f-4a88-b7e5-f3c66adb1f11}"
    SPEAK_MON_R = "Динамики (2- High Definition Audio Device)",\
        "{0.0.0.00000000}.{69f9cfe0-7cb7-4517-96ed-a816a26655f3}"
    SPEAK_MON_L = "BenQ EW2775ZH (Аудио Intel(R) для дисплеев)",\
        "{0.0.0.00000000}.{129de811-bfb3-4a98-96d3-0867c3ab5906}"
elif read_db_cell("pc") == 2:   # Домашний ПК
    SPEAK_HEAD_H = "Наушники (HONOR Magic Earbuds)", \
        "{0.0.0.00000000}.{5f0d3099-ef36-4600-af3a-ea4f1886dedd}"
    SPEAK_HEAD_S = "Headset (2- SB Tactic3D Rage Wireless)",\
        "{0.0.0.00000000}.{93389548-8b7a-48a2-bd56-7c3ac4101744}"
    SPEAK_HEAD_A = "Bloody G575 (3- USB Audio Device)", \
        "{0.0.0.00000000}.{838b3556-45e2-4242-a1f9-428fa1b06433}"
    SPEAK_MON_R = "DELL S2316H (NVIDIA High Definition Audio)",\
        "{0.0.0.00000000}.{1a6e09ed-9668-41da-b347-a5ce8fb88003}"

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

    'bot_about': 'bot_about(update, context)',
    'bot_settings': 'bot_settings(update, context)',
    'bot_changes_upd': 'bot_changes(update, context)',

    'multi': 'multi_menu(update, context)',
    'power': 'power_menu(update, context)',
    'clipboard': 'clipboard_menu(update, context)',
    'screen': 'screen_menu(update, context)',

    'op_tabs': 'tabs_menu(update, context)',

    'vpn': 'vpn_menu(update, context)',
    'sdai_link': 'sdai_links_menu(update, context)',
    'st_games': 'games_menu(update, context)',

    'script': 'scripts_menu(update, context)',
    'scr_eft': 'scr_eft_menu(update, context)'
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
    'tab_left': ('ctrl', 'pgup'),
    'tab_right': ('ctrl', 'pgdn'),
    'tab_prev': ('alt', 'left'),
    'tab_next': ('alt', 'right'),
    'tab_off': ('ctrl', 'w'),
    'tab_return': ('ctrl', 'shift', 't')
}

filler = '==================================\n'.replace('=', r'\=')
