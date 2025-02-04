# -*- coding: utf-8 -*-
import asyncio
import datetime
import sqlite3

import flet as ft
from loguru import logger
from telethon.errors import (UserBannedInChannelError, PeerIdInvalidError, MsgIdInvalidError, SlowModeWaitError,
                             ChatWriteForbiddenError, ChatGuestSendForbiddenError, FloodWaitError, ChannelPrivateError,
                             AuthKeyUnregisteredError)
from telethon.tl.types import PeerChannel

from src.config_handler import db_path
from src.db_handler import reading_from_the_channel_list_database
from src.subscribe import SUBSCRIBE
from src.telegram_client import find_files


class TelegramCommentator:
    """
    Класс для автоматизированной работы с комментариями в Telegram-каналах.
    """

    async def reading_json_file(self):
        """Чтение данных из json файла."""

        json_files = find_files(directory_path="data/message/", extension='json')

        with open(f'{json_files[0]}', 'r', encoding='utf-8') as file:
            data = file.read()
            logger.info(data)
        return data

    async def record_bottom_messages_database(self, message_id, channel_id) -> None:
        """Запись данных сообщения в базу данных."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Создаем таблицу для хранения информации о каналах, если она еще не существует
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS messages_channels (message_id, message_peer_id)''')
        cursor.execute('INSERT INTO messages_channels (message_id, message_peer_id) VALUES (?, ?)',
                       (message_id, channel_id))
        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()

    async def check_message_exists(self, message_id, channel_id) -> bool:
        """Проверяет существование сообщения в базе данных."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT 1 FROM messages_channels WHERE message_id = ? AND message_peer_id = ?',
            (message_id, channel_id)
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    async def write_comments_in_telegram(self, client, page: ft.Page, lv) -> None:
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

                    # Получаем ID сообщения и ID канала, чтобы записать данные в базу данных
                    message_id = message.id
                    message_peer_id = message.peer_id

                    lv.controls.append(ft.Text(
                        f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date}"))  # отображаем сообщение в ListView
                    page.update()  # Обновляем страницу

                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name[0], None):
                            last_message_ids[name[0]] = post.id

                            try:
                                if isinstance(message_peer_id, PeerChannel):
                                    channel_id = message_peer_id.channel_id

                                    # Проверяем существование записи в БД
                                    if not await self.check_message_exists(message_id, channel_id):
                                        data = await self.reading_json_file()
                                        logger.info(f"Сообщение для рассылки: {data}")
                                        await client.send_message(entity=name[0], message=f'{data}',
                                                                  comment_to=post.id)
                                        lv.controls.append(ft.Text(f'Наш комментарий: {data}'))  # отображаем сообщение в ListView
                                        page.update()  # Обновляем страницу

                                        lv.controls.append(ft.Text("Спим 5 секунд"))  # отображаем сообщение в ListView
                                        page.update()  # Обновляем страницу
                                        await asyncio.sleep(5)

                                    else:
                                        lv.controls.append(ft.Text(f"Комментарий к сообщению {message_id} уже был отправлен", color=ft.colors.GREEN))
                                        page.update()
                                        lv.controls.append(ft.Text("Спим 5 секунд"))  # отображаем сообщение в ListView
                                        page.update()  # Обновляем страницу
                                        await asyncio.sleep(5)

                                if isinstance(message_peer_id, PeerChannel):
                                    channel_id = message_peer_id.channel_id
                                    logger.info(f"{message_id}, {channel_id}")

                                    await self.record_bottom_messages_database(message_id, channel_id)

                            except ChatWriteForbiddenError:
                                lv.controls.append(ft.Text(
                                    f"Вы не можете отправлять сообщения в: {name[0]}"))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу

                            except MsgIdInvalidError:
                                lv.controls.append(
                                    ft.Text("Возможно пост был изменен или удален"))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу

                            except UserBannedInChannelError:
                                lv.controls.append(ft.Text(f"Вам запрещено отправлять сообщения в супергруппы/каналы",
                                                           color=ft.colors.RED))
                                page.update()  # Обновляем страницу

                            except SlowModeWaitError as e:
                                lv.controls.append(ft.Text(
                                    f"Вы не можете отправлять сообщения в супергруппы/каналы. Попробуйте позже через {str(datetime.timedelta(seconds=e.seconds))}",
                                    color=ft.colors.RED))
                                page.update()
                                lv.controls.append(ft.Text(f"Спим {str(datetime.timedelta(seconds=e.seconds))}", color=ft.colors.RED))
                                page.update()
                                await asyncio.sleep(e.seconds)

                            except FloodWaitError as e:
                                lv.controls.append(
                                    ft.Text(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}',
                                            color=ft.colors.RED))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу
                                lv.controls.append(
                                    ft.Text(f"Спим {str(datetime.timedelta(seconds=e.seconds))}", color=ft.colors.RED))
                                page.update()
                                await asyncio.sleep(5)

                            except ChatGuestSendForbiddenError:
                                lv.controls.append(ft.Text(f"Вы не можете отправлять сообщения в супергруппы/каналы",
                                                           color=ft.colors.RED))
                                page.update()  # Обновляем страницу

                            except ChannelPrivateError:
                                lv.controls.append(ft.Text(f"Канал {name[0]} закрыт",
                                                           color=ft.colors.RED))  # отображаем сообщение в ListView
                                page.update()  # Обновляем страницу

                            except PeerIdInvalidError:
                                lv.controls.append(ft.Text(f"Неверный ID канала: {name[0]}"))
                                page.update()


            except FloodWaitError as e:  # Если ошибка при подписке
                lv.controls.append(ft.Text(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}',
                                           color=ft.colors.RED))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                lv.controls.append(ft.Text(f"Спим {str(datetime.timedelta(seconds=e.seconds))}", color=ft.colors.RED))
                page.update()
                await asyncio.sleep(5)

            except AuthKeyUnregisteredError:  # Если аккаунт заблочен
                lv.controls.append(
                    ft.Text("Аккаунт заблокирован", color=ft.colors.RED))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                break

            except ChannelPrivateError:
                lv.controls.append(ft.Text(f"Канал {name[0]} закрыт",
                                           color=ft.colors.RED))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу