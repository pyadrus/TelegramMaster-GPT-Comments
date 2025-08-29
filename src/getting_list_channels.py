# -*- coding: utf-8 -*-
import flet as ft
from loguru import logger
from telethon.helpers import TotalList

from src.core.buttons import create_buttons
from src.core.views import program_title, view_with_elements
from src.db_handler import creating_a_channel_list
from src.telegram_client import connect_telegram_account


async def handle_getting_list_channels(page: ft.Page):
    """Создает страницу Получение списка каналов"""
    logger.info("Пользователь перешел на страницу Получение списка каналов")
    lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)

    # Добавляем пояснительный текст
    lv.controls.append(
        ft.Text(
            "Для получения списка каналов, необходимо подключить аккаунт к комментатору.\n\n"
            "🔗 Перед началом работы убедитесь, что ваш аккаунт успешно подключен. "
            "Подробнее об этом можно узнать в разделе 'Подключение аккаунтов'.\n\n"
            "🔄 После успешного подключения программа автоматически выведет список каналов, "
            "на которые подписан данный аккаунт.\n\n"
            "💾 Все данные будут сохранены в базе данных по пути: `data/database/app.db`\n",
        )
    )

    page.controls.append(
        lv
    )  # добавляем ListView на страницу для отображения информации
    page.views.clear()  # Очищаем страницу и добавляем новый View

    async def action_1(_):
        """ "Получение списка каналов"""
        try:
            lv.controls.append(
                ft.Text("Получение списка каналов...")
            )  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
            client = await connect_telegram_account()
            dialogs: TotalList = await client.get_dialogs()

            # Запись полученных каналов и групп в базу данных
            username_diclist = await creating_a_channel_list(
                dialogs
            )  # Создаем или подключаемся к базе данных SQLite

            for username in username_diclist:
                logger.info(username)
                lv.controls.append(
                    ft.Text(f"Найден канал: {username}")
                )  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу после каждого добавления
            await client.disconnect()  # Завершаем работу клиента
            lv.controls.append(
                ft.Text("✅ Получение списка каналов завершено.")
            )  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
        except Exception as e:
            logger.error(e)
            lv.controls.append(
                ft.Text(f"❌ Ошибка: {str(e)}")
            )  # отображаем ошибку в ListView
            page.update()  # Обновляем страницу

    await view_with_elements(
        page=page,
        title=await program_title(title="Получение списка каналов"),
        buttons=[
            await create_buttons(text="📋 Получить список каналов", on_click=action_1),
            await create_buttons(text="⬅ Назад", on_click=lambda _: page.go("/")),
        ],
        route_page="getting_list_channels",
        lv=lv,
    )
    page.update()  # Обновляем страницу
