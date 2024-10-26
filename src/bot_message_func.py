from typing import Optional

import telegram
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from definitions.services.menu_controls import menu_controls


async def send_bot_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    message_text: str,
    disable_link_preview: bool = True,
    reply_markup: Optional[telegram.InlineKeyboardMarkup] = None,
    parse_mode: Optional[str] = "MarkdownV2",
) -> None:

    chat_id = (update.message.chat_id if update.message else update.callback_query.message.chat_id)
    filler = menu_controls.filler
    filler = filler.replace("=", r"\=")
    text = filler + message_text

    if parse_mode == "MarkdownV2":
        parse_mode = telegram.constants.ParseMode.MARKDOWN_V2
    elif parse_mode == "HTML":
        parse_mode = telegram.constants.ParseMode.HTML
    else:
        parse_mode = telegram.constants.ParseMode.MARKDOWN

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_web_page_preview=disable_link_preview,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


async def edit_bot_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    message_text: str,
    disable_link_preview: bool = True,
    reply_markup: Optional[telegram.InlineKeyboardMarkup] = None,
    parse_mode: Optional[str] = None,
) -> None:

    chat_data = update.message or update.callback_query.message
    chat_id = chat_data.chat_id
    filler = menu_controls.filler
    if parse_mode is None:
        parse_mode = "MarkdownV2"
    if parse_mode == "MarkdownV2":
        filler = filler.replace("=", r"\=")
        parse_mode = telegram.constants.ParseMode.MARKDOWN_V2
    elif parse_mode == "HTML":
        parse_mode = telegram.constants.ParseMode.HTML
    else:
        parse_mode = telegram.constants.ParseMode.MARKDOWN

    text = filler + message_text
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=chat_data.message_id,
        text=text,
        disable_web_page_preview=disable_link_preview,
        reply_markup=InlineKeyboardMarkup(reply_markup),
        parse_mode=parse_mode,
    )
