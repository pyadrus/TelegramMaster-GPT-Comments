import tkinter as tk


def log_message(message: str, text_widget: tk.Text):
    """
    Выводит сообщение в текстовое поле.

    :param message: Текст сообщения.
    :param text_widget: Виджет Text для вывода.
    """
    text_widget.insert(tk.END, f"{message}\n")  # Добавляем текст
    text_widget.see(tk.END)  # Автоматический скролл к последней строке
