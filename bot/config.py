"""Конфигурация бота: загрузка токена из файла .env."""

import os

from dotenv import load_dotenv


def load_bot_token() -> str:
    """Загружает BOT_TOKEN из переменных окружения и проверяет его.

    Returns:
        Токен бота.

    Raises:
        RuntimeError: Если токен не задан в файле .env.
    """
    # Загружаем переменные окружения из файла .env (если он есть).
    load_dotenv()
    # Токен читается только из переменных окружения, хардкода в коде нет.
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Создайте файл .env по примеру .env.example "
            "и укажите в нём токен бота."
        )
    return token


# Токен бота для использования в main.py.
BOT_TOKEN: str = load_bot_token()
