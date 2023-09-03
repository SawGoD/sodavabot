import telegram
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup

from blocks.s_path import filler


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

◼️ - полный экран
◾️ - активный монитор
▪️ - активное приложение
'''


power = '''*Питание*

🔄 - перезагрузка ПК_(15 секунд)_
⭕ - выключение ПК_(15 секунд)_
🚫 - отмена действий питания

💤 - режим гибернации
🙈 - выключение мониторов
'''


additional_pc_menu = '''*Дополнительно*

🗂️ - перезапуск проводника
'''


def hints_menu(update, context):
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
