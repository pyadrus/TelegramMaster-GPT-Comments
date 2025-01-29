# -*- coding: utf-8 -*-
import os
from loguru import logger
from telethon import TelegramClient

from src import db_handler
from src.config_handler import api_id, api_hash
from src.connect import reading_proxy_data_from_the_database


def find_files(directory_path: str, extension: str) -> list:
    """
    Поиск файлов с определенным расширением в директории. Расширение файла должно быть указано без точки.

    :param directory_path: Путь к директории
    :param extension: Расширение файла (указанное без точки)
    :return list: Список имен найденных файлов
    """
    entities = []  # Список для хранения имен найденных файлов
    try:
        for file_name in os.listdir(directory_path):
            if file_name.endswith(f".{extension}"):  # Проверяем, заканчивается ли имя файла на заданное расширение
                file_path = os.path.join(directory_path, file_name)  # Полный путь к файлу
                entities.append(file_path)  # Добавляем путь к файлу в список

        logger.info(f"🔍 Найденные файлы: {entities}")  # Выводим имена найденных файлов
        return entities  # Возвращаем список путей к файлам
    except FileNotFoundError:
        logger.error(f"❌ Ошибка! Директория {directory_path} не найдена!")
        return []  # Возвращаем пустой список, если директория не найдена


async def connect_telegram_account() -> TelegramClient:
    """
    Подключается к Telegram аккаунту, используя api_id и api_hash.

    :return: TelegramClient объект, подключенный к Telegram.
    :raises: Exception, если не удалось подключиться ни к одному аккаунту.
    """
    session_files = find_files(directory_path="data/accounts/", extension='session')
    if not session_files:
        raise Exception("❌ Не найдено ни одного файла сессии в директории data/accounts/.")

    for session_file in session_files:
        client = TelegramClient(
            session=session_file,  # Полный путь к файлу сессии
            api_id=api_id,  # Идентификатор API Telegram
            api_hash=api_hash,  # Ключ API Telegram
            system_version="4.16.30-vxCUSTOM",
            proxy=await reading_proxy_data_from_the_database(db_handler)

        )
        logger.info(f'Попытка подключения к {session_file}')
        try:
            await client.connect()  # Попытка подключения к Telegram

            # Проверяем, авторизован ли пользователь
            if await client.is_user_authorized():
                logger.info(f'✅ Успешное подключение к {session_file}')
                return client
            else:
                logger.warning(f'❌ Аккаунт {session_file} не авторизован.')
                await client.disconnect()  # ` Если аккаунт не авторизован, выходим
        except Exception as e:
            logger.error(f'❌ Ошибка при подключении к {session_file}: {e}')
            if client.is_connected():
                await client.disconnect()  # Если аккаунт не авторизован, выходим

    # Если ни один аккаунт не подключился, выбрасываем исключение
    raise Exception("❌ Не удалось подключиться ни к одному аккаунту.")
