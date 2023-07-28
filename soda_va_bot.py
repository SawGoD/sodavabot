import os
import sys
import time
from blocks import u_send_logs
from dotenv import load_dotenv
from blocks.s_scripts_list import thread_script_eft_1, thread_script_eft_2, thread_script_eft_3
from blocks.b_computer import thread_speed_test
from blocks.b_command import start, restart
from blocks.u_common_func import ver_greet
from blocks.u_core_func import handle_text, button
from telegram.error import NetworkError, Unauthorized
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

thread_script_eft_1.start()
thread_script_eft_2.start()
thread_script_eft_3.start()

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


def main():
    with open(r'.\logs\error_py.txt', 'w', encoding='utf-8') as f:
        sys.stderr = f
        python = sys.executable
        try:
            while True:
                try:
                    ver_greet()
                    thread_speed_test.start()
                    updater = Updater(f'{TOKEN}', use_context=True)
                    dp = updater.dispatcher
                    dp.add_handler(CommandHandler('start', start))
                    dp.add_handler(CommandHandler('restart', restart))
                    dp.add_handler(CallbackQueryHandler(button))
                    dp.add_handler(MessageHandler(Filters.text, handle_text, run_async=True))
                    updater.start_polling()
                    updater.idle()
                    pass
                except NetworkError:
                    # Обработка ошибки "потеря соединения"
                    u_send_logs.log_form_cmd(update=None, context=None, cmd="Подключение", effect="отсутствует",
                                             action="Перезапуск")
                    time.sleep(5)
                    os.execv(python, [python, fr".\soda_va_bot.py"])
                except Unauthorized:
                    # Обработка ошибки "неавторизованный доступ"
                    u_send_logs.log_form_cmd(update=None, context=None, cmd="Токен", effect="неверный",
                                             action="Ожидание перезапуска")
                    # Общая обработка всех остальных ошибок
                except Exception as e:
                    u_send_logs.log_form_cmd(update=None, context=None, cmd="Ошибка", effect=f"'{e}'",
                                             action="Ожидание перезапуска")
                    time.sleep(5)
        except Exception as e:
            sys.stderr.write(str(e))


if __name__ == '__main__':
    main()
