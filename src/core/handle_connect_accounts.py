# -*- coding: utf-8 -*-
import flet as ft
from loguru import logger

from src.connect import TGConnect
from src.core.buttons import create_buttons
from src.core.views import program_title, view_with_elements


async def handle_connect_accounts(page: ft.Page):
    """Меню подключения аккаунтов"""
    try:
        logger.info("Пользователь перешел на страницу Подключение аккаунтов")
        page.views.clear()
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)

        async def _add_connect_accounts_message():
            """Добавляет стартовое сообщение в ListView."""
            lv.controls.append(
                ft.Text(
                    "⚙️ Подключение аккаунтов доступно двумя способами:\n\n"
                    "1. По номеру телефона\n"
                    "2. С использованием session-файлов\n\n"
                    "📱 Для подключения по номеру телефона:\n"
                    "- Укажите номер\n"
                    "- Введите код подтверждения\n"
                    "- При необходимости введите пароль\n\n"
                    "📂 Для подключения через session-файл:\n"
                    "- Загрузите готовый session-файл\n\n"
                    "⚠️ Важно: Храните session-файлы в безопасности!"
                )
            )
            page.update()

        async def connection_session_account(_):
            """Подключение session аккаунта"""
            lv.controls.append(ft.Text("📂 Подключение session аккаунта"))
            page.update()
            await TGConnect().connecting_session_accounts(
                page=page,
            )

        async def phone_connection(_):
            """Подключение аккаунтов по номеру телефона"""
            lv.controls.append(ft.Text("📱 Подключение по номеру телефона"))
            page.update()
            await TGConnect().connecting_number_accounts(page=page)

        # Добавляем стартовое сообщение
        await _add_connect_accounts_message()

        # Создаем вид с элементами
        await view_with_elements(
            page=page,
            title=await program_title(title="🔗 Подключение аккаунтов"),
            buttons=[
                await create_buttons(text="📂 Подключение session аккаунта", on_click=connection_session_account),
                await create_buttons(text="📱 Подключение по номеру телефона", on_click=phone_connection),
                await create_buttons(text="🔙 Назад", on_click=lambda _: page.go("/"))
            ],
            route_page="change_name_description_photo",
            lv=lv  # Передаем ListView для отображения
        )
        page.update()
    except Exception as e:
        logger.exception(e)
