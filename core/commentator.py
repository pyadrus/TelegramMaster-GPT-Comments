import datetime
import time
import tkinter as tk

import telethon
from loguru import logger
from rich.progress import track
from telethon.tl.functions.channels import JoinChannelRequest

from core.telegram_client import connect_telegram_account
from gui.log_message import log_message


class TelegramCommentator:
    """
    Класс для автоматизированной работы с комментариями в Telegram-каналах.

    :param config: Объект configparser.ConfigParser, содержащий настройки.
    """

    def __init__(self, config) -> None:
        self.config = config
        self.client = None

    def subscribe_to_channel(self, client, channel_name) -> None:
        """
        Подписывается на Telegram-канал.

        :param channel_name: Имя канала Telegram.
        :param client: TelegramClient объект.
        """
        try:
            client(JoinChannelRequest(channel_name))
            logger.info(f'Подписка на канал {channel_name} выполнена успешно.')
        except Exception as e:
            logger.exception(f'Ошибка при подписке на канал {channel_name}')

    def write_comments_in_telegram(self, client, channels, text_widget: tk.Text) -> None:
        """
        Пишет комментарии в указанных Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        :param client: TelegramClient объект.
        :param text_widget: Виджет Text для вывода.
        """
        last_message_ids = {name: 0 for name in channels}
        for name in channels:
            self.subscribe_to_channel(client, channel_name=name)  # Подписываемся на канал перед отправкой комментария
            try:
                channel_entity = self.client.get_entity(name)
                messages = self.client.get_messages(channel_entity, limit=1)
                for message in messages:
                    log_message(
                        f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date} Сообщение: {message.message}",
                        text_widget)
                    text_widget.update()

                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name, None):
                            last_message_ids[name] = post.id
                            message = 'Россия лучшая страна!'
                            try:
                                self.client.send_message(entity=name, message=message, comment_to=post.id)
                                log_message(f'Наш комментарий: {message}', text_widget)
                                text_widget.update()
                                for i in track(range(400), description="Перерыв в рассылке..."):
                                    time.sleep(1)
                            except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                                log_message(f"Вы не можете отправлять сообщения в: {name}", text_widget)
                            except telethon.errors.rpcerrorlist.MsgIdInvalidError:
                                log_message("Возможно пост был изменен или удален", text_widget)
                            except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                                log_message(
                                    "Вам запрещено отправлять сообщения в супергруппы/каналы (вызвано SendMessageRequest)",
                                    text_widget)
                            except telethon.errors.rpcerrorlist.FloodWaitError as e:
                                log_message(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}',
                                            text_widget)
                                time.sleep(e.seconds)
                            except telethon.errors.rpcerrorlist.ChatGuestSendForbiddenError as e:
                                log_message(str(e), text_widget)
                            except telethon.errors.rpcerrorlist.ChannelPrivateError:
                                log_message(f"Канал {name} закрыт", text_widget)
            except telethon.errors.rpcerrorlist.FloodWaitError as e:  # Если ошибка при подписке
                log_message(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}', text_widget)
                time.sleep(e.seconds)
            except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError:  # Если аккаунт заблочен
                log_message("Аккаунт заблокирован", text_widget)
                break

    def run(self, channels, text_widget: tk.Text) -> None:
        """
        Запускает процесс комментирования в Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        :param text_widget: Виджет Text для вывода.
        """
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))
        while True:
            self.write_comments_in_telegram(self.client, channels, text_widget)
