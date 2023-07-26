import os
import json


def create_main_db():
    filepath = ".\\data\\s_main_db.json"
    if not os.path.exists(filepath):
        data = {
            "sound_status": 1,
            "log_status": 1,
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
            "menu_range": {
                "min": 0,
                "max": 5,
                "last": 30
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


def crete_env():
    filepath = '.env'
    if not os.path.exists(filepath):
        data = "BOT_TOKEN=repalce\n" \
               "ALLOWED_USERS={'replace', 'replace', '334969852'}\n" \
               "LOG_IGNORED_USERS={'replace', 'replace', '334969852'}\n" \
               "LOG_OUTPUT=replace\n" \
               "LOG_ALERT={'screen', 'scrn_full', 'scrn_mon', 'scrn_app', 'logger'}\n" \
               "STEAM_LOGIN=replace\n" \
               "STEAM_PASS=replace\n"\
               "API_TOKEN=replace\n"
        with open('.env', 'w') as file:
            file.write(data)
