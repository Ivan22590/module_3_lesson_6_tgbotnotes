"""Клавиатуры бота: текстовые константы кнопок и меню."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Тексты кнопок главного меню (вынесены в константы, чтобы не дублировать).
BTN_ADD_TASK = "➕ Добавить задачу"
BTN_TASK_LIST = "📋 Список задач"
BTN_EXPORT_CSV = "📄 Экспорт CSV"

# Текст кнопки отмены на время ввода текста задачи.
BTN_CANCEL = "❌ Отмена"


def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню: крупные кнопки с фиксированным размером."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ADD_TASK)],
            [KeyboardButton(text=BTN_TASK_LIST)],
            [KeyboardButton(text=BTN_EXPORT_CSV)],
        ],
        resize_keyboard=True,
    )


def cancel_menu() -> ReplyKeyboardMarkup:
    """Клавиатура, которая показывается на время ввода текста задачи."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True,
    )
