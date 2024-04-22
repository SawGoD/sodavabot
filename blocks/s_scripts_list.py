import threading
import time

import keyboard
import pyautogui

from blocks.u_handle_db import read_db_cell

sdb_path = "s_scripts_db.json"


# ESCAPE FROM TARKOV 1
def buyer():
    pyautogui.FAILSAFE = False
    x_pos = read_db_cell("seft_1_set", filename=sdb_path)['x_pos']
    y_pos = read_db_cell("seft_1_set", filename=sdb_path)['y_pos']
    value = f'{read_db_cell("seft_1_set", filename=sdb_path)["value"]}'
    while True:
        if read_db_cell("script_eft_1", filename=sdb_path) == 1:
            if keyboard.is_pressed('space'):
                pyautogui.click(button='left')
                pyautogui.moveTo(x_pos, y_pos)
                time.sleep(0.05)
                pyautogui.write(value)
                pyautogui.click(button='left')
        else:
            # print("Script disabled")
            time.sleep(1)


# ESCAPE FROM TARKOV 2
def simple_clicker():
    pyautogui.FAILSAFE = False
    x_pos_1 = read_db_cell("seft_2_set", filename=sdb_path)['x_pos_1']
    y_pos_1 = read_db_cell("seft_2_set", filename=sdb_path)['y_pos_1']
    x_pos_2 = read_db_cell("seft_2_set", filename=sdb_path)['x_pos_2']
    y_pos_2 = read_db_cell("seft_2_set", filename=sdb_path)['y_pos_2']
    x_pos_3 = read_db_cell("seft_2_set", filename=sdb_path)['x_pos_3']
    y_pos_3 = read_db_cell("seft_2_set", filename=sdb_path)['y_pos_3']
    x_pos_4 = read_db_cell("seft_2_set", filename=sdb_path)['x_pos_4']
    y_pos_4 = read_db_cell("seft_2_set", filename=sdb_path)['y_pos_4']
    while True:
        if read_db_cell("script_eft_2", filename=sdb_path) == 1:
            if keyboard.is_pressed('s'):
                pyautogui.moveTo(x_pos_1, y_pos_1)
                pyautogui.click(button='left')
                pyautogui.moveTo(x_pos_2, y_pos_2)
                pyautogui.click(button='left')
                # time.sleep(0.05)
            if keyboard.is_pressed('esc'):
                pyautogui.moveTo(x_pos_3, y_pos_3)
                pyautogui.click(button='left')
                pyautogui.moveTo(x_pos_4, y_pos_4)
                pyautogui.click(button='left')
                pyautogui.write('56')
                pyautogui.moveTo(x_pos_3, y_pos_3)
                pyautogui.click(button='left')
                pyautogui.press('left')
                pyautogui.press('enter')
                # time.sleep(0.05)
        else:
            # print("Script disabled")
            time.sleep(1)


# ESCAPE FROM TARKOV 3
def holder3():
    while True:
        if read_db_cell("script_eft_3", filename=sdb_path) == 1:
            print("Script enabled")
        # if keyboard.is_pressed('space'):
            # pyautogui.click(button='left')
            pyautogui.moveTo(400, 375)
            time.sleep(0.1)
            # pyautogui.write('5')
            # pyautogui.click(button='left')
    else:
        print("Script disabled")
        time.sleep(1)


thread_script_eft_1 = threading.Thread(target=buyer)
thread_script_eft_2 = threading.Thread(target=simple_clicker)
thread_script_eft_3 = threading.Thread(target=holder3)
