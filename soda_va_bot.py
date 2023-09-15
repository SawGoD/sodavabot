import os
import sys
import time

from dotenv import load_dotenv
from telegram.error import NetworkError, Unauthorized
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from blocks import u_send_logs
from blocks.b_command import restart, start, get_threads
from blocks.b_computer import thread_speed_test, thread_check_health
from blocks.s_scripts_list import (thread_script_eft_1, thread_script_eft_2,
                                   thread_script_eft_3)
from blocks.u_common_func import restart_bot, ver_greet
from blocks.u_core_func import button, handle_text

thread_script_eft_1.start()
thread_script_eft_2.start()
thread_script_eft_3.start()
thread_check_health.start()

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

def main():
    with open(r'.\logs\error_py.txt', 'w', encoding='utf-8') as f:
        sys.stderr = f
        try:
            ver_greet()
            thread_speed_test.start()
            updater = Updater(f'{TOKEN}', use_context=True)
            dp = updater.dispatcher
            dp.add_handler(CommandHandler('start', start))
            dp.add_handler(CommandHandler('restart', restart))
            dp.add_handler(CommandHandler('get_threads', get_threads))
            dp.add_handler(CallbackQueryHandler(button))
            dp.add_handler(MessageHandler(
                Filters.text, handle_text, run_async=True))
            updater.start_polling()
            updater.idle()
            pass
        except NetworkError:
            # Обработка ошибки "потеря соединения"
            u_send_logs.log_form_cmd(update=None, context=None, cmd="Подключение", effect="отсутствует",
                                     action="Перезапуск")
            time.sleep(5)
            restart_bot()
        except Unauthorized:
            # Обработка ошибки "неавторизованный доступ"
            u_send_logs.log_form_cmd(update=None, context=None, cmd="Токен", effect="неверный",
                                     action="Ожидание перезапуска")
        except Exception as e:
            sys.stderr.write(str(e))


if __name__ == '__main__':
    main()
