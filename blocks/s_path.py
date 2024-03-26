import time

from blocks.s_file_gen import create_env, create_main_db
from blocks.u_common_func import get_path
from blocks.u_handle_db import read_db_cell

create_main_db()
create_env()
time.sleep(0.15)


SPEAK_MON_L, SPEAK_MON_R, SPEAK_HEAD_S, SPEAK_HEAD_A, SPEAK_HEAD_H = "", "", "", "", ""


SPEAK_HEAD_H = "Наушники (HONOR Magic Earbuds)"
SPEAK_HEAD_S = "Headset (3- SB Tactic3D Rage Wireless)"
SPEAK_HEAD_A = "Bloody G575 (3- USB Audio Device)"
SPEAK_MON_R = "DELL S2316H (NVIDIA High Definition Audio)"

DEFPATH = r'C:\Soda_VA_BOT'

# Путь для исполнения
BROWSER = get_path(r'Opera Software', 'Last Stable Install Path')+'launcher.exe'
STEAM = get_path(r'Valve\Steam', 'SteamPath')
VPN_PATH = get_path(r'Microsoft\Windows\CurrentVersion\Run', 'OpenVPN-GUI')
STEAMCMD = fr'{STEAM}\steamcmd.exe'
INCOGNITO = f'"{BROWSER}" --private'
NIRCMD = fr'{DEFPATH}/resource/nircmd.exe'

SCREENPATH = fr'{DEFPATH}\resource\screenshots'

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
    'bot_settings_admin': 'bot_settings_admin(update, context)',
    'bot_changes_upd': 'bot_changes(update, context)',

    'multi': 'multi_menu(update, context)',
    'health': 'health_menu(update, context)',
    'memory': 'memory_menu(update, context)',
    'additional_pc_menu': 'additional_pc_menu(update, context)',
    
    'op_tabs': 'tabs_menu(update, context)',

    'vpn': 'vpn_menu(update, context)',
    'sdai_link': 'sdai_links_menu(update, context)',
    'st_games': 'games_menu(update, context)',

    'script': 'scripts_menu(update, context)',
    'scr_eft': 'scr_eft_menu(update, context)'
}

dict_short_cmds = {
    'explorer_fix': 'explorer_fix()',
    'clear_clipboard': 'pyperclip.copy("")'
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
    'sdai_on': 'start "SDAI Monitor" A:/USD/webui-user.bat',
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
    'scrn_app': None,
    'scrn_full': -1,
    'scrn_1': 1, 'scrn_2': 2, 'scrn_3': 3,
    'scrn_4': 4, 'scrn_5': 5, 'scrn_6': 6,
    'scrn_7': 7, 'scrn_8': 8, 'scrn_9': 9
}

dict_of_num = {
    1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 
    4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 
    7: "7️⃣", 8: "8️⃣", 9: "9️⃣"
}


vpn_paths = {
    'vpn_1': "DE_Berlin-tcp.ovpn",
    'vpn_2': "LT_Vilnius-tcp.ovpn",
    'vpn_3': "TR_Istanbul-tcp.ovpn",
    'vpn_4': "DE_Frankfurt-udp.ovpn",
    'vpn_5': "UA_Kiev-udp.ovpn",
    'vpn_6': "FI_Helsinki-udp.ovpn"
}

tabs_hotkeys = {
    'tab_left': ('ctrl', 'pgup'),
    'tab_right': ('ctrl', 'pgdn'),
    'tab_prev': ('alt', 'left'),
    'tab_next': ('alt', 'right'),
    'tab_off': ('ctrl', 'w'),
    'tab_return': ('ctrl', 'shift', 't')
}

filler = '==================================\n'.replace('=', r'\=') # 34 символа
