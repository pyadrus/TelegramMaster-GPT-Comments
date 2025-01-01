import tkinter as tk

from loguru import logger
from rich import print

from config.config_handler import read_config
from core.commentator import TelegramCommentator
from core.profile_updater import change_profile_descriptions
from core.telegram_client import connect_telegram_account
from database.db_handler import reading_from_the_channel_list_database, creating_a_channel_list

logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы


def main(client) -> None:
    """
    Получает список диалогов (каналов, групп и т. д.) и создаёт базу данных.

    :param client: TelegramClient объект.
    """
    dialogs = client.get_dialogs()
    creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite
    client.disconnect()  # Завершаем работу клиента



