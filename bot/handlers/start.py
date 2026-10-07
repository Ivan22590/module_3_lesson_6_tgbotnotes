"""Обработчик команды /start."""

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.menus import main_menu

router = Router()

# Приветственный текст: кратко объясняет, что делает бот.
WELCOME_TEXT = (
    "Привет! Я бот для командной работы над задачами.\n"
    "Общий список задач доступен всем: добавляйте задачи, "
    "просматривайте список и выгружайте его в CSV-файл.\n\n"
    "Выберите действие в меню ниже."
)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Приветствует пользователя и показывает главное меню."""
    # Сбрасываем состояние, если пользователь находился в режиме добавления задачи.
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=main_menu())
