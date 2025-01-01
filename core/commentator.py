import datetime
import time

import telethon
from loguru import logger
from rich.progress import track
from telethon.tl.functions.channels import JoinChannelRequest

from core.telegram_client import connect_telegram_account


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

    def write_comments_in_telegram(self, client, channels) -> None:
        """
        Пишет комментарии в указанных Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        :param client: TelegramClient объект.
        """
        last_message_ids = {name: 0 for name in channels}
        for name in channels:

            self.subscribe_to_channel(client, channel_name=name)  # Подписываемся на канал перед отправкой комментария
            try:
                channel_entity = self.client.get_entity(name)
                messages = self.client.get_messages(channel_entity, limit=1)
                for message in messages:
                    logger.info(
                        f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date} Сообщение: {message.message}")

                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name, None):
                            last_message_ids[name] = post.id
                            message = 'Россия лучшая страна!'
                            try:
                                self.client.send_message(entity=name, message=message, comment_to=post.id)
                                logger.info(f'Наш комментарий: {message}')
                                for i in track(range(400), description="Перерыв в рассылке..."):
                                    time.sleep(1)
                            except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                                logger.info(f"Вы не можете отправлять сообщения в: {name}")
                            except telethon.errors.rpcerrorlist.MsgIdInvalidError:
                                logger.info("Возможно пост был изменен или удален")
                            except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                                logger.info("Вам запрещено отправлять сообщения в супергруппы/каналы "
                                            "(вызвано SendMessageRequest)")
                            except telethon.errors.rpcerrorlist.FloodWaitError as e:
                                logger.info(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}')
                                time.sleep(e.seconds)
                            except telethon.errors.rpcerrorlist.ChatGuestSendForbiddenError as e:
                                logger.info(e)
                            except telethon.errors.rpcerrorlist.ChannelPrivateError:
                                logger.info(f"Канал {name} закрыт")
            except telethon.errors.rpcerrorlist.FloodWaitError as e:  # Если ошибка при подписке
                logger.info(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}')
                time.sleep(e.seconds)
            except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError:  # Если аккаунт заблочен
                logger.info("Аккаунт заблокирован")
                break

    def run(self, channels) -> None:
        """
        Запускает процесс комментирования в Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        """
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))
        while True:
            self.write_comments_in_telegram(self.client, channels)
