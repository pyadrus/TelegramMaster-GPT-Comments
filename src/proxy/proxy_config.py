# -*- coding: utf-8 -*-
import os

from loguru import logger


def setup_proxy(proxy_user, proxy_password, proxy_ip, proxy_port) -> None:
    """
    Установка прокси

    :param proxy_user: username прокси
    :param proxy_password: password прокси
    :param proxy_ip: ip прокси
    :param proxy_port: port прокси
    :return: None
    """
    try:
        # Указываем прокси для HTTP и HTTPS
        os.environ["http_proxy"] = (
            f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}"
        )
        os.environ["https_proxy"] = (
            f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}"
        )
    except Exception as e:
        logger.exception(e)
