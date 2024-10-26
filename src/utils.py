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


def write_json(value: Any, *cells: str, filename: str = "titles_dict") -> None:
    with open(f"./data/{filename}.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        result = data
        for cell in cells[:-1]:
            result = result[cell]
        result[cells[-1]] = value
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()


async def get_new_state_json(cells: list, filename: str = "fleeting_data"):
    state = read_json(*cells, filename=filename)
    new_state = (1 - state if isinstance(state, int) else state)  # Проверка, является ли state целым числом
    write_json(new_state, *cells, filename=filename)
    print(f"New state of {cells}: {new_state}")


async def set_to_default_state():
    values = (
        "volume_expanded",
        "output_expanded",
    )
    for value in values:
        write_json(0, "summary_state", value, filename="fleeting_data")
    print("Set to default state")
