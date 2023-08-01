import winreg
import datetime
import random
import time
import pyglet
import sys
import os
from blocks.u_handle_db import read_db_cell, write_db_cell

# 2023      Март, апрель, май, июнь, июль, август
start_date = 1 + 1 + 1 + 1 + 1+1
ver = str(f'{start_date}.01b')


def sound_alert(filename):
    player = pyglet.media.Player()
    source = pyglet.media.load(f"./resource/sounds/{filename}")
    player.queue(source)
    player.play()
    time.sleep(2)


def restart_bot():
    python = sys.executable
    os.execv(python, [python, fr".\soda_va_bot.py"])


def ver_greet():
    daten, timen = clock()
    for i in range(1):
        print('')
    print("==================")
    print(f"Soda v{ver} started")
    print("Дата:", daten)
    print("Время:", timen)
    print("==================")
    print(f'Компьютер: {read_db_cell("cur_pc")[5:]}')
    if read_db_cell("sound_status") == 1:
        sound_alert("sound_greet.mp3")


def clock():
    now = datetime.datetime.now()
    now_date = now.strftime("%d.%m.%y")
    now_time = now.strftime('%H:%M:%S')
    return now_date, now_time


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


# Функция для устранения ошибки об отсутствии изменений
def mod_fix():
    result = ''
    for i in range(random.randint(5, 5)):
        result += random.choice('ㅤㅤㅤㅤㅤ     ')
        result += random.choice('     ㅤㅤㅤㅤㅤ')
    return result
