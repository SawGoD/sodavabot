import telegram
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup

from blocks.s_path import filler
from blocks.u_handle_db import write_db_cell

multi = '''*Мультимедиа*

🌀🎸🩸🖥 - устройства вывода

⏯ - пуск/пауза
⏪⏩ - -5сек/+5сек
⏮⏭ - предыдущий/следующий

50 - громкость 50
➖➕ - громкость -2/+2
🔊🔇- звук вкл/выкл
'''


screen = '''*Экран*

🔳 - полный экран
1️⃣ - монитор 1
2️⃣ - монитор 2
◾ - активное приложение
'''


power = '''*Питание*

🔄 - перезагрузка ПК_(15 секунд)_
⭕ - выключение ПК_(15 секунд)_
🚫 - отмена действий питания

💤 - режим гибернации
🙈 - выключение мониторов
'''

clipboard = '''*Буфер обмена*

🗑️ - Очистить буфер обмена
🔗 - Открыть ссылку из буфера

Чтобы отправить текст в буфер обмена, просто напишите сообщение боту в любом пункте меню\.

Кол-во символов для получения/отправки:
До: 4030/4096
'''


additional_pc_menu = '''*Дополнительно*

🗂️ - перезапуск проводника
'''


def hints_menu(update, context):
    write_db_cell("pc_health_check", 0, "check_status")
    write_db_cell("updater_status", 0)
    query = update.callback_query
    user_id = str(query.message.chat_id)
    if query.data == 'hints_power':
        back = 'power'
        mes = power
    elif query.data == 'hints_screen':
        back = 'screen'
        mes = screen
    elif query.data == 'hints_multi':
        back = 'multi'
        mes = multi
    elif query.data == 'hints_clipboard_menu':
        back = 'clipboard'
        mes = clipboard
    elif query.data == 'hints_additional_pc_menu':
        back = 'additional_pc_menu'
        mes = additional_pc_menu

    import re

    mes = re.sub(r'[-()+]', lambda x: '\\' + x.group(), mes)
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data=back),
         InlineKeyboardButton("🔝 Меню", callback_data='mmenu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"{filler}💡 {mes}",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
