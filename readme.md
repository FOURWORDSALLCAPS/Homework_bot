# TELEGRAM-бот для проверки работ на [DEVMAN](https://dvmn.org/)

Этот код представляет собой бота Telegram, который получает обновления из API Devman и отправляет уведомления пользователю в Telegram.

## Установка зависимостей

Запускаем CMD (можно через Win+R, дальше вводим cmd) и вписываем команду cd /D <путь к папке со скриптом>

```
pip install -r requirements.txt
```

## Запуск бота

```
python homework_bot.py
```

## Docker

- Установить [Docker](https://docs.docker.com/engine/install/)
- Собрать образ
```
docker build -t homework_bot .
```
 - Запустить контейнер
```
docker run -p 3000:5050 --env-file .env homework_bot
```

## Переменные окружения

Часть настроек берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `homework_bot.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 3 переменные:
- `DEVMAN_API_TOKEN` — Токен от [DEVMAN](https://dvmn.org/api/docs/)
- `TG_BOT_TOKEN` — Токен Telegram-бота, полученный через BotFather в Telegram
- `TG_CHAT_ID` — Идентификатор чата, полученный через @userinfobot в Telegram


## Версия Python: 
Я использовал Python `3.8.3`, но он должен работать на любой более новой версии.

## Цель проекта:
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

## Автор
(2023) Zaitsev Vladimir
