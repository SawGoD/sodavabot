from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from bot_callbacks.btns_template import bottom_keyboard, expand_btn
from bot_message_func import edit_bot_message
from definitions.services.computer_menu import (
    clipboard,
    multimedia,
    power,
    screen,
    state,
)
from definitions.services.main_menu import main_menu
from utils import get_new_state_json, mod_fix, read_json


async def computer_menu(update: Update, context: ContextTypes) -> None:

    reply_markup = [
        [
            InlineKeyboardButton(multimedia.title[:1], callback_data="multimedia_callback"),
            InlineKeyboardButton(screen.title[:1], callback_data="screen_callback"),
            InlineKeyboardButton(clipboard.title[:1], callback_data="clipboard_callback")
        ],
        [
            InlineKeyboardButton(state.title[:1], callback_data="state_callback"),
            InlineKeyboardButton(power.title[:1], callback_data="power_callback"),
        ],
    ]
    await edit_bot_message(
        update,
        context,
        message_text=main_menu.computer + mod_fix(),
        reply_markup=reply_markup + bottom_keyboard(),
    )


async def multimedia_menu(
    update: Update,
    context: ContextTypes,
    action: bool = False,
    act_type: str = None,
) -> None:
    if action:
        if act_type == "volume":
            await get_new_state_json(["buttons_data", "volume_state"])
            print("volume_new_state")
        if act_type == "vol_summary":
            await get_new_state_json(["summary_state", "volume_expanded"])
            print("vol_summary_new_state")
        if act_type == "output_summary":
            await get_new_state_json(["summary_state", "output_expanded"])
            print("output_summary_new_state")
    volume_state = read_json(filename="fleeting_data")["buttons_data"]["volume_state"]
    summary_state = read_json(filename="fleeting_data")["summary_state"]
    current_volume = read_json(filename="fleeting_data")["buttons_data"]["current_volume"]
    buttons_data = read_json(filename="fleeting_data")["buttons_data"]
    if volume_state == 1 and current_volume > 0:
        vol_state_text = multimedia.volon
    else:
        vol_state_text = multimedia.voloff
    reply_markup = [[
        InlineKeyboardButton(
            f"{buttons_data['current_device']} {buttons_data['current_volume']}%",
            callback_data="test_callback",
        ),
        expand_btn(summary_state["output_expanded"], "out_summary_callback"),
    ]]
    if summary_state["output_expanded"] == 1:
        reply_markup.append([
            InlineKeyboardButton("Device 1", callback_data="test_callback"),
            InlineKeyboardButton("Device 2", callback_data="test_callback"),
            InlineKeyboardButton("Device 3", callback_data="test_callback")
        ])
    reply_markup.append([
        InlineKeyboardButton(multimedia.previous, callback_data="previous_callback"),
        InlineKeyboardButton(multimedia.playpause, callback_data="playpause_callback"),
        InlineKeyboardButton(multimedia.next, callback_data="next_callback"),
    ])
    reply_markup.append([
        InlineKeyboardButton(multimedia.voldowm, callback_data="voldowm_callback"),
        InlineKeyboardButton(vol_state_text, callback_data="volstate_callback"),
        InlineKeyboardButton(multimedia.volup, callback_data="volup_callback"),
        expand_btn(summary_state["volume_expanded"], "vol_summary_callback"),
    ])
    if summary_state["volume_expanded"] == 1:
        reply_markup.append([
            InlineKeyboardButton("0", callback_data="vol_0"),
            InlineKeyboardButton("25", callback_data="vol_25"),
            InlineKeyboardButton("50", callback_data="vol_50"),
            InlineKeyboardButton("75", callback_data="vol_75"),
            InlineKeyboardButton("100", callback_data="vol_100"),
        ])
    await edit_bot_message(
        update,
        context,
        message_text=multimedia.title + mod_fix(),
        reply_markup=reply_markup + bottom_keyboard(back_btn="computer_callback"),
    )
