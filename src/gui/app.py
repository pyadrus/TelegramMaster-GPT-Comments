import flet as ft
from loguru import logger

from src.config.config_handler import read_config
from src.core.commentator import TelegramCommentator, log_messagess
from src.core.profile_updater import change_profile_descriptions
from src.core.telegram_client import connect_telegram_account
from src.database.db_handler import reading_from_the_channel_list_database


async def action_2_with_log(page: ft.Page, text_field: ft.Text):
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


async def action_3(page: ft.Page, text_field: ft.Text):
    """
    Изменяет имя, описание и фото профиля Telegram аккаунта.
    :return: None
    """
    log_messagess("Смена: имени, описания, фото профиля", text_field)  # Сообщаем об успехе
    config = await read_config()
    client = await connect_telegram_account(config.get("telegram_settings", "id"),
                                            config.get("telegram_settings", "hash"))
    await change_profile_descriptions(client, text_field)


async def action_4(page: ft.Page, text_field: ft.Text):
    """Подписка на каналы"""
    pass


async def action_5(page: ft.Page, text_field: ft.Text):
    """Формирование списка каналов"""
    pass
