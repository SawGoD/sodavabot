from telegram import InlineKeyboardButton

from definitions.services.menu_controls import menu_controls


def bottom_keyboard(back_btn: str = None) -> list:
    if back_btn:
        bottom_keyboard = [[
            InlineKeyboardButton(menu_controls.back, callback_data=back_btn),
            InlineKeyboardButton(menu_controls.menu, callback_data="goto_menu_callback"),
        ]]
    else:
        bottom_keyboard = [[InlineKeyboardButton(menu_controls.menu, callback_data="goto_menu_callback")]]
    return bottom_keyboard


def expand_btn(summary_state: int, callback: str = None) -> InlineKeyboardButton:
    if summary_state == 1:
        # print("expaned")
        btn = InlineKeyboardButton(
            menu_controls.collapse,
            callback_data=callback,
        )
    else:
        # print("collapsed")
        btn = InlineKeyboardButton(
            menu_controls.expand,
            callback_data=callback,
        )

    return btn
