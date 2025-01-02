from loguru import logger
from rich import print
import tkinter as tk
from config.config_handler import read_config
from core.commentator import TelegramCommentator
from core.profile_updater import change_profile_descriptions
from core.telegram_client import connect_telegram_account
from database.db_handler import reading_from_the_channel_list_database, creating_a_channel_list
from gui.log_message import log_message


def action_1_with_log(text_widget: tk.Text):
    """
    Получает список диалогов (каналов, групп и т. д.) и создаёт базу данных.
    Выводит информацию в текстовое поле.
    """
    try:
        log_message("Получение списка каналов...", text_widget)
        config = read_config()
        client = connect_telegram_account(config.get("telegram_settings", "id"),
                                          config.get("telegram_settings", "hash"))

        dialogs = client.get_dialogs()
        username_diclist = creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite
        for username in username_diclist:
            logger.info(username)
            log_message(f"Найден канал: {username}", text_widget)
        client.disconnect()  # Завершаем работу клиента
        log_message("Получение списка каналов завершено.", text_widget)
    except Exception as e:
        logger.exception(e)
        log_message(f"Ошибка: {e}", text_widget)


def action_2_with_log(text_widget: tk.Text):
    log_message("Отправка комментариев...", text_widget)
    try:
        config = read_config()
        results = reading_from_the_channel_list_database()
        usernames = [row[0] for row in results]  # Преобразуем результат в словарь
        logger.info(usernames)  # Логируем полученный список пользователей
        telegram_commentator = TelegramCommentator(config)  # Каналы с комментариями
        telegram_commentator.run(usernames, text_widget)
        log_message("Комментарии успешно отправлены.", text_widget)  # Сообщаем об успехе
    except Exception as e:
        logger.exception(e)
        log_message("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log",
                    text_widget)


def action_3():
    print("[bold red]Смена: имени, описания, фото профиля")
    config = read_config()
    client = connect_telegram_account(config.get("telegram_settings", "id"),
                                      config.get("telegram_settings", "hash"))
    change_profile_descriptions(client)


if __name__ == "__main__":
    action_3()
