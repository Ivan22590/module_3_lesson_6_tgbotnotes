"""Точка входа: настройка логирования, бота, роутеров и запуск polling."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.database.db import init_db
from bot.handlers import export, start, tasks


async def main() -> None:
    """Создаёт бота, подключает роутеры и запускает long polling."""
    # Базовое логирование.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Бот и диспетчер с хранилищем состояний в памяти (FSM).
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Порядок роутеров важен: сначала /start, затем экспорт (/list_csv),
    # затем задачи — внутри tasks.py обработчик ожидания текста идёт последним.
    dp.include_router(start.router)
    dp.include_router(export.router)
    dp.include_router(tasks.router)

    # Создаём базу данных и таблицу tasks при первом запуске.
    await init_db()

    logger.info("Бот запущен, начинаем long polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
