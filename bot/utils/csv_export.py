"""Экспорт списка задач в CSV-файл."""

import csv
import io


def build_csv(tasks: list[tuple[int, str, str, str]]) -> bytes:
    """Формирует содержимое CSV-файла со списком задач.

    Кодировка UTF-8 with BOM (utf-8-sig), чтобы файл нормально
    открывался в Excel. Разделитель — запятая.
    Внутри текста задачи запятые, кавычки и переносы строк
    экранируются автоматически модулем csv.

    Args:
        tasks: Список кортежей (id, text, user, created_at).

    Returns:
        Байты CSV-файла, готовые к отправке как документ.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=",")
    writer.writerow(["id", "text", "user", "created_at"])
    writer.writerows(tasks)
    # utf-8-sig добавляет BOM в начало файла для корректного
    # открытия CSV в Excel.
    return buffer.getvalue().encode("utf-8-sig")
