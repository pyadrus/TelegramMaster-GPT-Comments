import tkinter as tk

from loguru import logger
from rich import print

from config.config_handler import read_config
from core.commentator import TelegramCommentator
from core.profile_updater import change_profile_descriptions
from core.telegram_client import connect_telegram_account
from database.db_handler import reading_from_the_channel_list_database, creating_a_channel_list


def action_1():
    """
    Получает список диалогов (каналов, групп и т. д.) и создаёт базу данных.
    """
    print("[bold red]Получение списка каналов")
    config = read_config()
    client = connect_telegram_account(config.get("telegram_settings", "id"),
                                      config.get("telegram_settings", "hash"))

    dialogs = client.get_dialogs()
    creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite
    client.disconnect()  # Завершаем работу клиента


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
    action_1()
    action_2()
    action_3()
