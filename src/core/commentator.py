import datetime
import time

import flet as ft
import telethon
from faker.providers.bank.en_PH import logger
from rich.progress import track

from src.core.subscribe import SUBSCRIBE
from src.database.db_handler import reading_from_the_channel_list_database


class TelegramCommentator:
    """
    Класс для автоматизированной работы с комментариями в Telegram-каналах.
    """

    async def write_comments_in_telegram(self, client, page, lv) -> None:
        """
        Пишет комментарии в указанных Telegram-каналах.

        :param client: TelegramClient объект.
        :param page: Номер страницы.
        :param lv: Номер уровня.
        :return: None.
        """
        channels = await reading_from_the_channel_list_database()
        logger.info(channels)
        last_message_ids = {name: 0 for name in channels}
        for name in channels:
            logger.info(name)
            await SUBSCRIBE().subscribe_to_channel(client, name[0], page,
                                                   lv)  # Подписываемся на канал перед отправкой комментария
            try:
                channel_entity = await client.get_entity(name[0])
                messages = await client.get_messages(channel_entity, limit=1)
                for message in messages:
                    lv.controls.append(ft.Text(
                        f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date} Сообщение: {message.message}"))  # отображаем сообщение в ListView
                    page.update()  # Обновляем страницу

                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name[0], None):
                            last_message_ids[name[0]] = post.id
                            message = 'Россия лучшая страна!'
                            try:
                                await client.send_message(entity=name[0], message=message, comment_to=post.id)
                                lv.controls.append(
                                    ft.Text(f'Наш комментарий: {message}'))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                                for i in track(range(400), description="Перерыв в рассылке..."):
                                    time.sleep(1)
                            except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                                lv.controls.append(ft.Text(
                                    f"Вы не можете отправлять сообщения в: {name[0]}"))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                            except telethon.errors.rpcerrorlist.MsgIdInvalidError:
                                lv.controls.append(
                                    ft.Text("Возможно пост был изменен или удален"))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                            except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                                lv.controls.append(ft.Text(
                                    "Вам запрещено отправлять сообщения в супергруппы/каналы (вызвано SendMessageRequest)"))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                            except telethon.errors.rpcerrorlist.FloodWaitError as e:
                                lv.controls.append(ft.Text(
                                    f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}'))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                                time.sleep(e.seconds)
                            except telethon.errors.rpcerrorlist.ChatGuestSendForbiddenError as e:
                                lv.controls.append(ft.Text(str(e)))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                            except telethon.errors.rpcerrorlist.ChannelPrivateError:
                                lv.controls.append(
                                    ft.Text(f"Канал {name[0]} закрыт"))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
            except telethon.errors.rpcerrorlist.FloodWaitError as e:  # Если ошибка при подписке
                lv.controls.append(ft.Text(
                    f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}'))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                time.sleep(e.seconds)
            except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError:  # Если аккаунт заблочен
                lv.controls.append(ft.Text("Аккаунт заблокирован"))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                break
