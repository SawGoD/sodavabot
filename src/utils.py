import json
import os
import random
import sys
from typing import Any


def mod_fix():
    # Генерирует случайную строку для исправления ошибки
    result = ""
    for i in range(random.randint(4, 4)):
        result += random.choice("ㅤㅤㅤㅤㅤ     ")
        result += random.choice("     ㅤㅤㅤㅤㅤ")
    return result


def restart_bot():
    # Перезапускает бота
    python = sys.executable
    os.execv(python, [python, rf".\src\main.py"])


def read_json(*cells: str, filename: str = "titles_dict") -> Any:
    with open(f"./data/{filename}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        result = data
        for cell in cells:
            result = result[cell]
        return result
