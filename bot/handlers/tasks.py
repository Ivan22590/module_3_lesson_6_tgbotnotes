"""Обработчики задач: добавление (FSM), список и отмена."""

import logging

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.db import add_task, get_tasks
from bot.keyboards.menus import BTN_ADD_TASK, BTN_CANCEL, BTN_TASK_LIST, cancel_menu, main_menu
from bot.states import AddTaskStates

router = Router()

logger = logging.getLogger(__name__)

# Тексты сообщений бота.
ASK_TEXT = "Отправьте текст задачи одним сообщением."
TASK_ADDED = "Задача добавлена."
CANCELLED = "Добавление задачи отменено."
NOTHING_TO_CANCEL = "Сейчас нет активных действий для отмены."
WRONG_TEXT = "Пожалуйста, отправьте корректный текст задачи."
NON_TEXT_MESSAGE = "Пожалуйста, отправьте текст задачи текстовым сообщением."
NO_TASKS = "Задачи пока нет."
DB_ERROR = "Не удалось работать со списком задач. Попробуйте позже."


# --- Отмена ---


@router.message(or_f(Command("cancel"), F.text == BTN_CANCEL))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """Отменяет текущее действие и возвращает главное меню."""
    current_state = await state.get_state()
    if current_state is None:
        # Отменять нечего — пользователь не в процессе добавления.
        await message.answer(NOTHING_TO_CANCEL, reply_markup=main_menu())
        return
    # Очищаем состояние и возвращаем главное меню.
    await state.clear()
    await message.answer(CANCELLED, reply_markup=main_menu())


# --- Добавление задачи ---


@router.message(or_f(Command("add"), F.text == BTN_ADD_TASK))
async def cmd_add(message: Message, state: FSMContext) -> None:
    """Переводит пользователя в состояние ожидания текста задачи."""
    # Текст задачи бот попросит следующим сообщением.
    await state.set_state(AddTaskStates.waiting_for_text)
    await message.answer(ASK_TEXT, reply_markup=cancel_menu())


@router.message(AddTaskStates.waiting_for_text, F.text)
async def process_task_text(message: Message, state: FSMContext) -> None:
    """Принимает текст задачи, сохраняет её и возвращает главное меню."""
    # Команды (текст с "/") не сохраняем как задачу, а просим обычный текст.
    if message.text.startswith("/"):
        await message.answer(ASK_TEXT, reply_markup=cancel_menu())
        return

    # Убираем пробелы по краям и проверяем, что текст не пустой.
    task_text = message.text.strip()
    if not task_text:
        await message.answer(WRONG_TEXT, reply_markup=cancel_menu())
        return

    # Автор задачи: username, если его нет — полное имя.
    author = message.from_user.username or message.from_user.full_name

    try:
        await add_task(task_text, author)
    except Exception:
        # Логируем ошибку базы данных и просим попробовать позже.
        logger.exception("Не удалось сохранить задачу")
        await message.answer(DB_ERROR, reply_markup=cancel_menu())
        return

    # Задача сохранена: очищаем состояние и показываем главное меню.
    await state.clear()
    await message.answer(TASK_ADDED, reply_markup=main_menu())


@router.message(AddTaskStates.waiting_for_text)
async def process_non_text(message: Message) -> None:
    """Просит отправить задачу текстом, если пришло фото, стикер и т.п."""
    await message.answer(NON_TEXT_MESSAGE, reply_markup=cancel_menu())


# --- Список задач ---


@router.message(or_f(Command("list"), F.text == BTN_TASK_LIST))
async def cmd_list(message: Message, state: FSMContext) -> None:
    """Показывает все задачи из общего списка."""
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
        logger.exception("Не удалось получить список задач")
        await message.answer(DB_ERROR, reply_markup=markup)
        return

    if not tasks:
        await message.answer(NO_TASKS, reply_markup=markup)
        return

    # Формируем читаемый список: номер, текст, автор и дата создания.
    lines: list[str] = []
    for number, (_task_id, text, user, created_at) in enumerate(tasks, start=1):
        created_date = created_at.split("T")[0]
        lines.append(
            f"{number}. {text}\n"
            f"   Автор: {user}\n"
            f"   Дата: {created_date}"
        )

    await message.answer("Список задач:\n\n" + "\n\n".join(lines), reply_markup=markup)
