import tkinter as tk

from loguru import logger

from gui.app import action_1, action_2, action_3

logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы

if __name__ == "__main__":
    root = tk.Tk()
    program_version, date_of_program_change = "0.0.4", "01.01.2025"
    root.title(f"Версия {program_version}. Дата изменения {date_of_program_change}")
    root.geometry("400x200")

    btn_1 = tk.Button(root, text="Получение списка каналов", command=action_1)
    btn_1.pack(pady=10)
    btn_2 = tk.Button(root, text="Отправка комментариев", command=action_2)
    btn_2.pack(pady=10)
    btn_3 = tk.Button(root, text="Смена имени, описания, фото", command=action_3)
    btn_3.pack(pady=10)

    root.mainloop()
