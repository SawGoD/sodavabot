import os
from typing import Optional

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, filters

from bot_callbacks.buttons_handler import buttons_handler
from commands import restart, start

load_dotenv()

TOKEN: Optional[str] = str(os.getenv("TELEGRAM_TOKEN"))


def main():
    app = Application.builder().token(TOKEN).build()
    # Команды
    app.add_handler(CommandHandler("start", start, filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler("restart", restart, filters.ChatType.PRIVATE))

    # Обработчик кнопок
    app.add_handler(CallbackQueryHandler(buttons_handler))

    print("➖ ➖ ➖  Бот запущен➖ ➖ ➖")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
