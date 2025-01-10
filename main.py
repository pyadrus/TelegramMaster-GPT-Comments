import tkinter as tk
from tkinter import messagebox

from loguru import logger

from core.logging_in import loging
from src.gui.app import action_1_with_log, action_2_with_log, action_3, action_4, action_5
from src.core.configs import program_version, date_of_program_change

logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")  # Логирование программы


def show_author_info():
    """Отображает информацию об авторе."""
    messagebox.showinfo("Автор", "Разработчик: Ваше имя\nВерсия программы: " + program_version)


def display_settings(frame):
    """Обновляет содержимое окна для отображения настроек."""
    for widget in frame.winfo_children():
        widget.destroy()  # Удаляем текущие виджеты

    tk.Label(frame, text="Настройки программы", font=("Arial", 16)).pack(pady=20)
    tk.Button(frame, text="Назад", command=lambda: display_main_menu(frame)).pack(pady=20)


def display_main_menu(frame):
    """Обновляет содержимое окна для отображения основного меню."""
    for widget in frame.winfo_children():
        widget.destroy()  # Удаляем текущие виджеты

    # Определение текстового поля для вывода информации
    info_field = tk.Text(frame, width=30, height=10)  # Ширина 30 символов, высота 10 строк
    info_field.place(x=340, y=20, width=350, height=300)  # Размещение справа

    # Определение кнопок
    btn_1 = tk.Button(frame, text="Получение списка каналов", command=lambda: action_1_with_log(info_field))
    btn_1.place(x=50, y=20, width=250, height=50)

    btn_2 = tk.Button(frame, text="Отправка комментариев", command=lambda: action_2_with_log(info_field))
    btn_2.place(x=50, y=80, width=250, height=50)  # Задаем ширину и высоту кнопки

    btn_3 = tk.Button(frame, text="Смена имени, описания, фото", command=lambda: action_3(info_field))
    btn_3.place(x=50, y=140, width=250, height=50)  # Задаем ширину и высоту кнопки

    btn_4 = tk.Button(frame, text="Подписка на каналы", command=lambda: action_4(info_field))
    btn_4.place(x=50, y=200, width=250, height=50)  # Задаем ширину и высоту кнопки

    btn_5 = tk.Button(frame, text="Формирование списка каналов", command=lambda: action_5(info_field))
    btn_5.place(x=50, y=260, width=250, height=50)  # Задаем ширину и высоту кнопки


if __name__ == "__main__":
    loging()
    root = tk.Tk()

    root.title(f"Версия {program_version}. Дата изменения {date_of_program_change}")
    root.geometry("720x400")  # Увеличиваем ширину окна для текстового поля

    # Создание меню
    menu_bar = tk.Menu(root)

    # Добавление меню "Файл"
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Выход", command=root.quit)
    menu_bar.add_cascade(label="Файл", menu=file_menu)

    # Добавление меню "Помощь"
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Автор", command=show_author_info)
    help_menu.add_command(label="Настройки", command=lambda: display_settings(main_frame))
    menu_bar.add_cascade(label="Помощь", menu=help_menu)

    # Установка меню в окне
    root.config(menu=menu_bar)

    # Основной контейнер для содержимого
    main_frame = tk.Frame(root, width=720, height=400)
    main_frame.pack(fill="both", expand=True)

    # Отображение главного меню
    display_main_menu(main_frame)

    root.mainloop()
