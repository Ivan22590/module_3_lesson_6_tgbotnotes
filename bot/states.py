"""Состояния FSM бота."""

from aiogram.fsm.state import State, StatesGroup


class AddTaskStates(StatesGroup):
    """Состояния процесса добавления задачи."""

    # Ожидание текста задачи от пользователя.
    waiting_for_text = State()
