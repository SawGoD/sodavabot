import json
import random
from typing import Any


def mod_fix():
    # Генерирует случайную строку для исправления ошибки
    result = ""
    for i in range(random.randint(5, 5)):
        result += random.choice("ㅤㅤㅤㅤㅤ     ")
        result += random.choice("     ㅤㅤㅤㅤㅤ")
    return result


def read_json(*cells: str, filename: str = "titles_dict") -> Any:
    with open(f"./data/{filename}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        result = data
        for cell in cells:
            result = result[cell]
        return result
