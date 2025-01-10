import datetime
import time

import flet as ft
import telethon
from loguru import logger
from rich.progress import track
from telethon.tl.functions.channels import JoinChannelRequest

from src.core.telegram_client import connect_telegram_account


def log_messagess(message: str, text_field: ft.TextField):
    """
    Выводит сообщение в текстовое поле.
    :param message: Текст сообщения.
    :param text_field: Виджет TextField для вывода.
    :return: None
    """
    # Добавляем текст в конец текстового поля
    text_field.value += f"{message}\n"
    # Прокручиваем текстовое поле до последней строки
    text_field.focus()
    text_field.update()

class TelegramCommentator:
    """
    Класс для автоматизированной работы с комментариями в Telegram-каналах.

    :param config: Объект configparser.ConfigParser, содержащий настройки.
    """

    def __init__(self, config) -> None:
        self.config = config
        self.client = None

    async def subscribe_to_channel(self, client, channel_name) -> None:
        """
        Подписывается на Telegram-канал.
        :param channel_name: Имя канала Telegram.
        :param client: TelegramClient объект.
        :return: None.
        """
        try:
            await client(JoinChannelRequest(channel_name))
            logger.info(f'Подписка на канал {channel_name} выполнена успешно.')
        except Exception as e:
            logger.exception(f'Ошибка при подписке на канал {channel_name}')

    async def write_comments_in_telegram(self, client, channels, text_field: ft.TextField) -> None:
        """
        Пишет комментарии в указанных Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        :param client: TelegramClient объект.
        :param text_widget: Виджет Text для вывода.
        :return: None.
        """
        last_message_ids = {name: 0 for name in channels}
        for name in channels:
            await self.subscribe_to_channel(client, channel_name=name)  # Подписываемся на канал перед отправкой комментария
            try:
                channel_entity = self.client.get_entity(name)
                messages = self.client.get_messages(channel_entity, limit=1)
                for message in messages:
                    log_messagess(
                        f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date} Сообщение: {message.message}",
                        text_field)
                    text_field.update()

                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name, None):
                            last_message_ids[name] = post.id
                            message = 'Россия лучшая страна!'
                            try:
                                self.client.send_message(entity=name, message=message, comment_to=post.id)
                                log_messagess(f'Наш комментарий: {message}', text_field)
                                text_field.update()
                                for i in track(range(400), description="Перерыв в рассылке..."):
                                    time.sleep(1)
                            except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                                log_messagess(f"Вы не можете отправлять сообщения в: {name}", text_field)
                            except telethon.errors.rpcerrorlist.MsgIdInvalidError:
                                log_messagess("Возможно пост был изменен или удален", text_field)
                            except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                                log_messagess(
                                    "Вам запрещено отправлять сообщения в супергруппы/каналы (вызвано SendMessageRequest)",
                                    text_field)
                            except telethon.errors.rpcerrorlist.FloodWaitError as e:
                                log_messagess(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}',
                                            text_field)
                                time.sleep(e.seconds)
                            except telethon.errors.rpcerrorlist.ChatGuestSendForbiddenError as e:
                                log_messagess(str(e), text_field)
                            except telethon.errors.rpcerrorlist.ChannelPrivateError:
                                log_messagess(f"Канал {name} закрыт", text_field)
            except telethon.errors.rpcerrorlist.FloodWaitError as e:  # Если ошибка при подписке
                log_messagess(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}', text_field)
                time.sleep(e.seconds)
            except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError:  # Если аккаунт заблочен
                log_messagess("Аккаунт заблокирован", text_field)
                break

    async def run(self, channels, text_field: ft.TextField) -> None:
        """
        Запускает процесс комментирования в Telegram-каналах.
        :param channels: Список имен Telegram-каналов.
        :param text_field: Виджет TextField для вывода.
        :return: None
        """
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))
        while True:
            await self.write_comments_in_telegram(self.client, channels, text_field)
