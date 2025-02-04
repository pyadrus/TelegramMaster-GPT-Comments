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

from src.config_handler import db_path, time_config
from src.core.buttons import create_buttons
from src.core.views import program_title, view_with_elements
from src.db_handler import reading_from_the_channel_list_database
from src.subscribe import SUBSCRIBE
from src.telegram_client import connect_telegram_account
from src.telegram_client import find_files


class TelegramCommentator:
    """
    Класс для автоматизированной работы с комментариями в Telegram-каналах.
    """

    async def handle_submitting_comments(self, page: ft.Page):
        """Создает страницу Отправка комментариев"""
        try:
            logger.info("Пользователь перешел на страницу Отправка комментариев")
            page.views.clear()  # Очищаем страницу и добавляем новый View
            lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
            page.controls.append(lv)  # добавляем ListView на страницу для отображения информации

            async def action_1(_):
                lv.controls.append(ft.Text("Отправка комментариев"))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                client = await connect_telegram_account()
                await self.write_comments_in_telegram(client, page, lv)

            await view_with_elements(page=page, title=await program_title(title="Отправка комментариев"),
                                     buttons=[
                                         await create_buttons(text="Отправка комментариев", on_click=action_1),
                                         await create_buttons(text="Назад", on_click=lambda _: page.go("/"))
                                     ],
                                     route_page="submitting_comments", lv=lv)
            page.update()  # Обновляем страницу
        except Exception as e:
            logger.exception(e)

    async def message_output_program_window(self, lv: ft.ListView, page: ft.Page, message_program):
        """"Вывод сообщений в окно программы."""
        lv.controls.append(ft.Text(f"{message_program}", color=ft.colors.RED))  # отображаем сообщение в ListView
        page.update()  # Обновляем страницу

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

    async def write_comments_in_telegram(self, client, page: ft.Page, lv: ft.ListView) -> None:
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

                    await self.message_output_program_window(lv=lv, page=page,
                                                             message_program=f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date}")
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
                                        await client.send_message(entity=name[0], message=f'{data}',
                                                                  comment_to=post.id)
                                        await self.message_output_program_window(lv=lv, page=page,
                                                                                 message_program=f"Наш комментарий: {data}")
                                        await self.message_output_program_window(lv=lv, page=page,
                                                                                 message_program=f"Спим 5 секунд")
                                        await asyncio.sleep(int(time_config))
                                    else:
                                        await self.message_output_program_window(lv=lv, page=page,
                                                                                 message_program=f"Комментарий к сообщению {message_id} уже был отправлен")
                                        await self.message_output_program_window(lv=lv, page=page,
                                                                                 message_program=f"Спим 5 секунд")
                                        await asyncio.sleep(int(time_config))

                                if isinstance(message_peer_id, PeerChannel):
                                    channel_id = message_peer_id.channel_id
                                    logger.info(f"{message_id}, {channel_id}")

                                    await self.record_bottom_messages_database(message_id, channel_id)

                            except ChatWriteForbiddenError:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Вы не можете отправлять сообщения в: {name[0]}")
                            except MsgIdInvalidError:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Возможно пост был изменен или удален")
                            except UserBannedInChannelError:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Вам запрещено отправлять сообщения в супергруппы/каналы")
                            except SlowModeWaitError as e:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Вы не можете отправлять сообщения в супергруппы/каналы. Попробуйте позже через {str(datetime.timedelta(seconds=e.seconds))}")
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Спим {str(datetime.timedelta(seconds=e.seconds))}")
                                await asyncio.sleep(e.seconds)
                            except FloodWaitError as e:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}")
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Спим {str(datetime.timedelta(seconds=e.seconds))}")
                                await asyncio.sleep(int(time_config))
                            except ChatGuestSendForbiddenError:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Вы не можете отправлять сообщения в супергруппы/каналы")
                            except ChannelPrivateError:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Канал {name[0]} закрыт")
                            except PeerIdInvalidError:
                                await self.message_output_program_window(lv=lv, page=page,
                                                                         message_program=f"Неверный ID канала: {name[0]}")
            except FloodWaitError as e:  # Если ошибка при подписке
                await self.message_output_program_window(lv=lv, page=page,
                                                         message_program=f"Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}")
                await self.message_output_program_window(lv=lv, page=page,
                                                         message_program=f"Спим {str(datetime.timedelta(seconds=e.seconds))}")
                await asyncio.sleep(int(time_config))
            except AuthKeyUnregisteredError:  # Если аккаунт заблочен
                await self.message_output_program_window(lv=lv, page=page,
                                                         message_program=f"Аккаунт заблокирован")
                break

            except ChannelPrivateError:
                await self.message_output_program_window(lv=lv, page=page, message_program=f"Канал {name[0]} закрыт")
