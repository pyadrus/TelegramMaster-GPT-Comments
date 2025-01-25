from loguru import logger
from telethon.tl.functions.channels import JoinChannelRequest
import flet as ft


class SUBSCRIBE:
    """Класс подписки на группы и каналы Telegram"""

    async def subscribe_to_channel(self, client, channel_name, page, lv) -> None:
        """
        Подписывается на Telegram-канал.
        :param channel_name: Имя канала Telegram.
        :param client: TelegramClient объект.
        :return: None.
        """
        try:
            await client(JoinChannelRequest(channel_name))
            lv.controls.append(
                ft.Text(f"Подписка на канал {channel_name} выполнена успешно."))  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
        except Exception as e:
            logger.exception(f'Ошибка при подписке на канал {channel_name}')
