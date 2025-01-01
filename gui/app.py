import tkinter as tk

from loguru import logger
from rich import print

from config.config_handler import read_config
from core.commentator import TelegramCommentator
from core.profile_updater import change_profile_descriptions
from core.telegram_client import connect_telegram_account
from database.db_handler import reading_from_the_channel_list_database, creating_a_channel_list


def action_1():
    print("[bold red]Получение списка каналов")
    config = read_config()
    client = connect_telegram_account(config.get("telegram_settings", "id"),
                                      config.get("telegram_settings", "hash"))
    main(client)


def action_2():
    print("[bold red]Отправка комментариев")
    try:
        config = read_config()
        results = reading_from_the_channel_list_database()
        usernames = [row[0] for row in results]  # Преобразуем результат в словарь
        logger.info(usernames)  # Выводим полученный словарь
        telegram_commentator = TelegramCommentator(config)  # Каналы с комментариями
        telegram_commentator.run(usernames)
    except Exception as e:
        logger.exception(e)
        logger.info("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")


def action_3():
    print("[bold red]Смена: имени, описания, фото профиля")
    config = read_config()
    client = connect_telegram_account(config.get("telegram_settings", "id"),
                                      config.get("telegram_settings", "hash"))
    change_profile_descriptions(client)


if __name__ == "__main__":
    # Создаем главное окно
    root = tk.Tk()
    program_version, date_of_program_change = "0.0.4", "01.01.2025"  # Версия программы, дата изменения
    root.title(f"Версия {program_version}. Дата изменения {date_of_program_change}")  # Описание окна
    root.geometry("400x200")  # Размер окна ширина, высота

    # Создаем кнопки
    btn_1 = tk.Button(root, text="Получение списка каналов", command=action_1)
    btn_1.pack(pady=10)
    btn_2 = tk.Button(root, text="Отправка комментариев", command=action_2)
    btn_2.pack(pady=10)
    btn_3 = tk.Button(root, text="Смена имени, описания, фото", command=action_3)
    btn_3.pack(pady=10)

    # Запускаем главный цикл приложения
    root.mainloop()
