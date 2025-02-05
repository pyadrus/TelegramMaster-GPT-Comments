# -*- coding: utf-8 -*-
from loguru import logger

from src.telegram_client import find_files


async def reading_json_file():
    """Чтение данных из json файла."""

    json_files = find_files(directory_path="data/message/", extension='json')

    with open(f'{json_files[0]}', 'r', encoding='utf-8') as file:
        data = file.read()
        logger.info(data)
    return data
