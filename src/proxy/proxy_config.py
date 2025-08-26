# -*- coding: utf-8 -*-
import os

from loguru import logger

from src.config import proxy_user, proxy_password, proxy_ip, proxy_port


def setup_proxy():
    try:
        # Указываем прокси для HTTP и HTTPS
        os.environ['http_proxy'] = f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}"
        os.environ['https_proxy'] = f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}"
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    setup_proxy()
