"""Работа с базой данных задач: SQLite через aiosqlite.

База создаётся автоматически при первом запуске.
Все SQL-запросы параметризованные, чтобы избежать SQL-инъекций.
"""

import logging
from datetime import datetime, timezone
from pathlib import Path

import aiosqlite

# Путь к файлу базы данных (рядом с main.py).
DB_PATH = Path(__file__).resolve().parents[2] / "tasks.db"

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Создаёт базу данных и таблицу tasks, если их ещё нет."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.commit()
    logger.info("База данных готова: %s", DB_PATH)


async def add_task(text: str, user: str) -> None:
    """Добавляет задачу в общий список.

    Args:
        text: Текст задачи.
        user: Автор задачи (username или полное имя).
    """
    # Дата создания в формате ISO с указанием часового пояса.
    created_at = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
            (text, user, created_at),
        )
        await db.commit()


async def get_tasks() -> list[tuple[int, str, str, str]]:
    """Возвращает все задачи из общего списка.

    Returns:
        Список кортежей: (id, text, user, created_at).
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id, text, user, created_at FROM tasks ORDER BY id") as cursor:
            rows = await cursor.fetchall()
    return [(row["id"], row["text"], row["user"], row["created_at"]) for row in rows]
