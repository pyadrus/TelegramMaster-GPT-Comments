# -*- coding: utf-8 -*-
import datetime
import time

import flet as ft
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest


class SUBSCRIBE:
    """Класс подписки на группы и каналы Telegram"""

    async def subscribe_to_channel(self, client, channel_name, page: ft.Page, lv) -> None:
        """
        Подписывается на Telegram-канал.
        :param channel_name: Имя канала Telegram.
        :param client: TelegramClient объект.
        :param page: Страница приложения.
        :param lv: ListView.
        :return: None.
        """
        if not channel_name or channel_name.isdigit():
            lv.controls.append(ft.Text(f"Неверный username канала: {channel_name}", color=ft.colors.RED))
            page.update()
            return

        try:
            await client(JoinChannelRequest(channel_name))
            lv.controls.append(ft.Text(f"Успешная подписка на {channel_name}", color=ft.colors.RED))
            page.update()
        except FloodWaitError as e:
            lv.controls.append(ft.Text(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}',
                                       color=ft.colors.RED))  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
            time.sleep(e.seconds)
