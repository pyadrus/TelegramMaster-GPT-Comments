# -*- coding: utf-8 -*-
import asyncio
import datetime

import flet as ft
from loguru import logger
from telethon.errors import (UserBannedInChannelError, PeerIdInvalidError, MsgIdInvalidError, SlowModeWaitError,
                             ChatWriteForbiddenError, ChatGuestSendForbiddenError, FloodWaitError, ChannelPrivateError,
                             AuthKeyUnregisteredError)
from telethon.tl.types import PeerChannel

from src.ai import get_groq_response
from src.config_handler import time_config
from src.core.buttons import create_buttons
from src.core.views import program_title, view_with_elements, message_output_program_window
from src.db_handler import reading_from_the_channel_list_database, check_message_exists, record_bottom_messages_database
from src.subscribe import SUBSCRIBE
from src.telegram_client import connect_telegram_account




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

            # Добавляем пояснительный текст
            lv.controls.append(ft.Text(
                "🔗 Перед началом работы убедитесь, что все необходимые настройки выполнены.\n\n"
                "🔄 В процессе работы программа будет отображать важную информацию для пользователя.\n\n"
                "💾 Обработанные сообщения автоматически сохраняются в базе данных: `data/database/app.db`\n",
            ))

            page.controls.append(lv)  # добавляем ListView на страницу для отображения информации

            async def action_1(_):
                lv.controls.append(ft.Text("Отправка комментариев"))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                await self.write_comments_in_telegram(await connect_telegram_account(), page, lv)

            await view_with_elements(page=page, title=await program_title(title="Отправка комментариев"),
                                     buttons=[
                                         await create_buttons(text="Отправка комментариев", on_click=action_1),
                                         await create_buttons(text="Назад", on_click=lambda _: page.go("/"))
                                     ],
                                     route_page="submitting_comments", lv=lv)
            page.update()  # Обновляем страницу
        except Exception as e:
            logger.exception(e)

    async def write_comments_in_telegram(self, client, page: ft.Page, lv: ft.ListView) -> None:
        """
        Пишет комментарии в указанных Telegram-каналах.

        :param client: TelegramClient объект.
        :param page: Номер страницы.
        :param lv: Номер уровня.
        :return: None.
        """
        channels = await reading_from_the_channel_list_database()
        last_message_ids = {name: 0 for name in channels}
        for name in channels:
            logger.info(name[0])
            await SUBSCRIBE(page).subscribe_to_channel(client, name[0], lv)  # Подписываемся на канал перед отправкой комментария
            try:
                messages = await client.get_messages(await client.get_entity(name[0]), limit=1)
                for message in messages:

                    # Получаем ID сообщения и ID канала, чтобы записать данные в базу данных
                    message_id = message.id
                    message_peer_id = message.peer_id
                    message_text = message.text
                    await message_output_program_window(lv=lv, page=page, message_program=f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date}")
                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name[0], None):
                            last_message_ids[name[0]] = post.id

                            try:
                                if isinstance(message_peer_id, PeerChannel):
                                    channel_id = message_peer_id.channel_id
                                    data = await get_groq_response(message_text)
                                    # Проверяем существование записи в БД
                                    if not await check_message_exists(message_id, channel_id):
                                        # Если записи нет, отправляем комментарий и записываем его в БД

                                        # Заранее заготовленное сообщение
                                        # data = await reading_json_file()
                                        # Получаем текст сообщения от ИИ

                                        await client.send_message(entity=name[0], message=f'{data}',
                                                                  comment_to=post.id)
                                        await message_output_program_window(lv=lv, page=page,
                                                                            message_program=f"Наш комментарий: {data}")
                                        await message_output_program_window(lv=lv, page=page,
                                                                            message_program=f"Спим {time_config} секунд")
                                        await asyncio.sleep(int(time_config))
                                    else:
                                        await message_output_program_window(lv=lv, page=page,
                                                                            message_program=f"Комментарий к сообщению {message_id} уже был отправлен")
                                        await message_output_program_window(lv=lv, page=page,
                                                                            message_program=f"Спим {time_config} секунд")
                                        await asyncio.sleep(int(time_config))

                                if isinstance(message_peer_id, PeerChannel):
                                    channel_id = message_peer_id.channel_id
                                    logger.info(f"{message_id}, {channel_id}")

                                    await record_bottom_messages_database(message_id, channel_id)

                            except ChatWriteForbiddenError:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Вы не можете отправлять сообщения в: {name[0]}")
                            except MsgIdInvalidError:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Возможно пост был изменен или удален")
                            except UserBannedInChannelError:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Вам запрещено отправлять сообщения в супергруппы/каналы")
                            except SlowModeWaitError as e:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Вы не можете отправлять сообщения в супергруппы/каналы. Попробуйте позже через {str(datetime.timedelta(seconds=e.seconds))}")
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Спим {str(datetime.timedelta(seconds=e.seconds))}")
                                await asyncio.sleep(e.seconds)
                            except FloodWaitError as e:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}")
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Спим {str(datetime.timedelta(seconds=e.seconds))}")
                                await asyncio.sleep(int(time_config))
                            except ChatGuestSendForbiddenError:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Вы не можете отправлять сообщения в супергруппы/каналы")
                            except ChannelPrivateError:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Канал {name[0]} закрыт")
                            except PeerIdInvalidError:
                                await message_output_program_window(lv=lv, page=page,
                                                                    message_program=f"Неверный ID канала: {name[0]}")
            except FloodWaitError as e:  # Если ошибка при подписке
                await message_output_program_window(lv=lv, page=page,
                                                    message_program=f"Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}")
                await message_output_program_window(lv=lv, page=page,
                                                    message_program=f"Спим {str(datetime.timedelta(seconds=e.seconds))}")
                await asyncio.sleep(int(time_config))
            except AuthKeyUnregisteredError:  # Если аккаунт заблочен
                await message_output_program_window(lv=lv, page=page,
                                                    message_program=f"Аккаунт заблокирован")
                break

            except ChannelPrivateError:
                await message_output_program_window(lv=lv, page=page, message_program=f"Канал {name[0]} закрыт")
