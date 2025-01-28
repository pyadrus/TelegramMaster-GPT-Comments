# -*- coding: utf-8 -*-
import flet as ft
from telethon.tl.functions.channels import JoinChannelRequest


class SUBSCRIBE:
    """Класс подписки на группы и каналы Telegram"""

    async def subscribe_to_channel(self, client, channel_name, page, lv) -> None:
        """
        Подписывается на Telegram-канал.
        :param channel_name: Имя канала Telegram.
        :param client: TelegramClient объект.
        :param page: Страница приложения.
        :param lv: ListView.
        :return: None.
        """

        await client(JoinChannelRequest(channel_name))
        lv.controls.append(
            ft.Text(f"Подписка на канал {channel_name} выполнена успешно."))  # отображаем сообщение в ListView
        page.update()  # Обновляем страницу
