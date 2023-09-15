import json
import os


def create_main_db():
    filepath = ".\data\s_main_db.json"
    if not os.path.exists(filepath):
        data = {
            "sound_status": 1,
            "log_status": 1,
            "hints_status": 1,
            "updater_status": 0,
            "pc": 2,
            "cur_pc": "👩🏻‍💻 Домашний ПК",
            "volume_status": 1,
            "output_device": "",
            "pc_health_check": {
                "check_status": 0,
                "cpu": 0,
                "ram": 0
            },
            "volume": {
                "head_h": 0,
                "head_s": 0,
                "head_a": 0,
                "mon_r": 0,
                "mon_l": 0
            },
            "menu_range": {
                "repo": "sodavabot",
                "min": 0,
                "max": 5,
                "page": 6,
                "last": 30
            },
            "admin_only": {
                "screen_state": 1,
                "power_state": 1
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


def create_env():
    filepath = '.env'
    if not os.path.exists(filepath):
        data = "BOT_TOKEN=repalce\n" \
               "ALLOWED_USERS={'replace', 'replace', '334969852'}\n" \
               "ADMIN_USERS={'replace', 'replace', '334969852'}\n" \
               "LOG_IGNORED_USERS={'replace', 'replace', '334969852'}\n" \
               "LOG_OUTPUT=replace\n" \
               "LOG_ALERT={'screen', 'scrn_full', 'scrn_mon', 'scrn_app', 'logger'}\n" \
               "STEAM_LOGIN=replace\n" \
               "STEAM_PASS=replace\n" \
               "API_TOKEN_GIT=replace\n" \
               "API_TOKEN=replace\n"
        with open(filepath, 'w') as file:
            file.write(data)
            
            
create_main_db()
create_env()
