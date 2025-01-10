from loguru import logger
import flet as ft
from src.config.config_handler import read_config
from src.core.commentator import TelegramCommentator, log_messagess
from src.core.profile_updater import change_profile_descriptions
from src.core.telegram_client import connect_telegram_account
from src.database.db_handler import reading_from_the_channel_list_database, creating_a_channel_list


async def action_1_with_log(text_field: ft.TextField):
    """
    Получает список диалогов (каналов, групп и т. д.), создает базу данных и выводит информацию в текстовое поле.

    :param text_field: Виджет Text для вывода логов и сообщений пользователю.
    :return: None
    """
    try:
        log_messagess("Получение списка каналов...", text_field)
        config = await read_config()
        client = await connect_telegram_account(config.get("telegram_settings", "id"),
                                                config.get("telegram_settings", "hash"))

        dialogs = await client.get_dialogs()
        username_diclist = await creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite
        for username in username_diclist:
            logger.info(username)
            log_messagess(f"Найден канал: {username}", text_field)
        await client.disconnect()  # Завершаем работу клиента
        log_messagess("Получение списка каналов завершено.", text_field)
    except Exception as e:
        logger.exception(e)
        log_messagess(f"Ошибка: {e}", text_field)


async def action_2_with_log(text_field: ft.TextField):
    """
    Отправляет комментарии к постам каналов из базы данных и выводит информацию в текстовое поле.

    :param text_field: Виджет Text для вывода логов и сообщений пользователю.
    :return: None
    """
    log_messagess("Отправка комментариев...", text_field)
    try:
        config = await read_config()
        results = await reading_from_the_channel_list_database()
        usernames = [row[0] for row in results]  # Преобразуем результат в словарь
        logger.info(usernames)  # Логируем полученный список пользователей
        telegram_commentator = TelegramCommentator(config)  # Каналы с комментариями
        await telegram_commentator.run(usernames, text_field)
        log_messagess("Комментарии успешно отправлены.", text_field)  # Сообщаем об успехе
    except Exception as e:
        logger.exception(e)
        log_messagess("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log",
                      text_field)


async def action_3(text_field: ft.TextField):
    """
    Изменяет имя, описание и фото профиля Telegram аккаунта.
    :return: None
    """
    log_messagess("Смена: имени, описания, фото профиля", text_field)  # Сообщаем об успехе
    config = await read_config()
    client = await connect_telegram_account(config.get("telegram_settings", "id"),
                                            config.get("telegram_settings", "hash"))
    await change_profile_descriptions(client, text_field)


async def action_4(info_field):
    """Подписка на каналы"""
    pass


async def action_5(info_field):
    """Формирование списка каналов"""
    pass
