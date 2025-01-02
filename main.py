import tkinter as tk

from loguru import logger

import __version__
from gui.app import action_1_with_log, action_2_with_log, action_3

logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы

if __name__ == "__main__":
    root = tk.Tk()

    root.title(f"Версия {__version__}. Дата изменения {__version__.__date__}")
    root.geometry("720x250")  # Увеличиваем ширину окна для текстового поля

    # Определение текстового поля для вывода информации
    info_field = tk.Text(root, width=30, height=10)  # Ширина 30 символов, высота 10 строк
    info_field.place(x=360, y=20, width=350, height=200)  # Размещение справа

    # Определение кнопок
    btn_1 = tk.Button(root, text="Получение списка каналов", command=lambda: action_1_with_log(info_field))
    btn_1.place(x=50, y=20, width=250, height=50)

    btn_2 = tk.Button(root, text="Отправка комментариев", command=lambda: action_2_with_log(info_field))
    btn_2.place(x=50, y=80, width=250, height=50)  # Задаем ширину и высоту кнопки

    btn_3 = tk.Button(root, text="Смена имени, описания, фото", command=action_3)
    btn_3.place(x=50, y=140, width=250, height=50)  # Задаем ширину и высоту кнопки

    root.mainloop()
