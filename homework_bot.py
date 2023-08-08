import time
import telegram
import requests

from environs import Env


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
    timestamp = None

    while True:
        try:
            result = get_updates(api_token, timestamp)
            lesson_url = result['new_attempts'][0]['lesson_url']
            lesson_title = result['new_attempts'][0]['lesson_title']
            if result.get("status") == "timeout":
                timestamp = result.get("timestamp_to_request")
            elif result['new_attempts'][0]['is_negative']:
                bot.send_message(text=f'Название урока: {lesson_title}\nСсылка: {lesson_url}'
                                      f'\nК сожалению, в работе нашлись ошибки!', chat_id=tg_chat_id)
            else:
                bot.send_message(text=f'Название урока: {lesson_title}\nСсылка: {lesson_url}'
                                      f'\nПреподавателю всё понравилось, можно приступать к следующему уроку!',
                                 chat_id=tg_chat_id)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Соединение разорвано')
            time.sleep(5)


if __name__ == '__main__':
    main()
