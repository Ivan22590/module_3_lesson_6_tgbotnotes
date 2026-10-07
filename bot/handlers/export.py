"""Обработчик экспорта задач в CSV-файл."""

import logging

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message

from bot.database.db import get_tasks
from bot.keyboards.menus import BTN_EXPORT_CSV, cancel_menu, main_menu
from bot.states import AddTaskStates
from bot.utils.csv_export import build_csv

router = Router()

logger = logging.getLogger(__name__)

# Тексты сообщений бота.
NO_TASKS_FOR_EXPORT = "Задач пока нет, поэтому нечего экспортировать."
EXPORT_ERROR = "Не удалось подготовить или отправить файл. Попробуйте позже."

# Имя файла, который получит пользователь.
CSV_FILENAME = "tasks.csv"


@router.message(or_f(Command("list_csv"), F.text == BTN_EXPORT_CSV))
async def cmd_export(message: Message, state: FSMContext) -> None:
    """Формирует CSV-файл со всеми задачами и отправляет его документом."""
    # Если пользователь всё ещё вводит задачу — оставляем кнопку отмены,
    # иначе возвращаем главное меню.
    current = await state.get_state()
    markup = (
        cancel_menu()
        if current == AddTaskStates.waiting_for_text.state
        else main_menu()
    )

    try:
        tasks = await get_tasks()
    except Exception:
        # Логируем ошибку базы данных.
        logger.exception("Не удалось получить задачи для экспорта")
        await message.answer(EXPORT_ERROR, reply_markup=markup)
        return

    # Пустой файл не отправляем.
    if not tasks:
        await message.answer(NO_TASKS_FOR_EXPORT, reply_markup=markup)
        return

    try:
        csv_bytes = build_csv(tasks)
        file = BufferedInputFile(csv_bytes, filename=CSV_FILENAME)
        await message.answer_document(file, reply_markup=markup)
    except Exception:
        # Логируем ошибку отправки файла.
        logger.exception("Не удалось отправить CSV-файл")
        await message.answer(EXPORT_ERROR, reply_markup=markup)
