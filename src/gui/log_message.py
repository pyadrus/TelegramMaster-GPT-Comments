import flet as ft


def log_message(message: str, text_field: ft.TextField):
    """
    Выводит сообщение в текстовое поле.
    :param message: Текст сообщения.
    :param text_field: Виджет TextField для вывода.
    :return: None
    """
    # Добавляем текст в конец текстового поля
    text_field.value += f"{message}\n"
    # Прокручиваем текстовое поле до последней строки
    text_field.focus()
    text_field.update()
