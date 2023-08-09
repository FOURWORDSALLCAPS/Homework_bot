import time
import telegram
import requests
import logging
import traceback

from textwrap import dedent
from environs import Env


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_updates(api_token, timestamp=None):
    url = "https://dvmn.org/api/long_polling/"

    headers = {
        'Authorization': f'Token {api_token}'
    }
    params = {
        "timestamp": timestamp
    }
    response = requests.get(url, headers=headers, params=params, timeout=60)

    return response.json()


def main():
    env = Env()
    env.read_env()
    api_token = env('DEVMAN_API_TOKEN')
    tg_bot_token = env('TG_BOT_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    bot = telegram.Bot(token=tg_bot_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    bot.logger.warning('Бот успешно запущен!')
    timestamp = None
    while True:
        try:
            review = get_updates(api_token, timestamp)
            new_attempt = review['new_attempts'][0]
            lesson_url = new_attempt['lesson_url']
            lesson_title = new_attempt['lesson_title']
            if review.get("status") == "timeout":
                timestamp = review.get("timestamp_to_request")
            elif new_attempt['is_negative']:
                text = f'''
                    Название урока: {lesson_title}
                    Ссылка: {lesson_url}
                    К сожалению, в работе нашлись ошибки!
                    '''
                bot.send_message(text=dedent(text), chat_id=tg_chat_id)
            else:
                text = f'''
                    Название урока: {lesson_title}
                    Ссылка: {lesson_url}
                    Преподавателю всё понравилось, можно приступать к следующему уроку!'''
                bot.send_message(text=dedent(text), chat_id=tg_chat_id)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Соединение разорвано')
            time.sleep(5)


if __name__ == '__main__':
    main()
