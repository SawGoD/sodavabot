import datetime
import os
import random
import re
import sys
import time
import winreg

import pyglet

from blocks.u_handle_db import read_db_cell, write_db_cell

def sound_alert(filename):
    # Воспроизводит звуковой сигнал
    player = pyglet.media.Player()
    source = pyglet.media.load(f"./resource/sounds/{filename}")
    player.queue(source)
    player.play()
    time.sleep(2)


def restart_bot():
    # Перезапускает бота
    python = sys.executable
    os.execv(python, [python, fr".\soda_va_bot.py"])


def get_version():
    with open('README.md', 'r', encoding='utf-8') as file:
        first_line = file.readline()
        match = re.search(r'v(\d+\.\d+\w+)', first_line)
        if match:
            ver = match.group(1)
            return ver


def ver_greet():
    # Выводит приветствие с версией и текущей датой и временем
    daten, timen = clock()
    for i in range(1):
        print('')
    print("==================")
    print(f"Soda v{get_version()} started")
    print("Дата:", daten)
    print("Время:", timen)
    print("==================")
    print(f'Компьютер: {read_db_cell("cur_pc")[5:]}')
    if read_db_cell("sound_status") == 1:
        sound_alert("sound_greet.mp3")


def clock():
    # Возвращает текущую дату и время
    now = datetime.datetime.now()
    now_date = now.strftime("%d.%m.%y")
    now_time = now.strftime('%H:%M:%S')
    return now_date, now_time


def get_path(path, file):
    # Открывает ключ реестра, содержащий информацию о приложении Steam
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        fr"Software\{path}")
    value, reg_type = winreg.QueryValueEx(key, file)
    # Возвращает найденный путь
    return value


def user_input(s, h_type):
    # Записывает в базу данных ожидаемый пользовательский ввод и тип обработки
    write_db_cell("waiting_input", s)
    write_db_cell("handle_type", h_type)


# Функция для устранения ошибки об отсутствии изменений
def mod_fix():
    # Генерирует случайную строку для исправления ошибки
    result = ''
    for i in range(random.randint(5, 5)):
        result += random.choice('ㅤㅤㅤㅤㅤ     ')
        result += random.choice('     ㅤㅤㅤㅤㅤ')
    return result
