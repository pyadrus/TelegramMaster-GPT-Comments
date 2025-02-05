# -*- coding: utf-8 -*-
import flet as ft
from loguru import logger

from src.core.buttons import create_buttons
from src.core.views import program_title, view_with_elements
from src.core.views import view_with_elements_input_field
from src.db_handler import read_channel_list_from_database
from src.db_handler import save_channels_to_db
from src.subscribe import SUBSCRIBE
from src.telegram_client import connect_telegram_account


async def handle_settings(page: ft.Page):
    logger.info("Пользователь перешел на страницу Настройки")
    page.views.clear()
    lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
    page.controls.append(lv)

    lv.controls.append(
        ft.Text(
            "🔗 Подключение прокси — настройка подключения через прокси (SOCKS5). Вам потребуется указать IP-адрес, порт, а также логин и пароль.\n\n"
            "⏳ Запись времени — настройка задержек между отправкой сообщений и подпиской на каналы. Укажите время в секундах для безопасной работы.\n\n"
            "🆔 Запись ID и Hash — ввод API ID и API Hash для авторизации в Telegram. Можно получить в https://my.telegram.org/apps.\n\n"
            "✉️ Запись сообщения — настройка текста, который будет отправляться в комментариях. Можно задать любой текст для автоматической рассылки.\n\n"
        )
    )
    page.update()

    async def connection_proxy(_):
        """🔗 Подключение прокси"""
        page.go("/settings_proxy")

    async def record_time(_):
        """⏳ Запись времени"""
        page.go("/record_time")

    async def record_id_hash(_):
        """🆔 Запись ID и Hash"""
        page.go("/record_id_hash")

    async def recording_message(_):
        """✉️ Запись сообщения"""
        page.go("/recording_message")

    await view_with_elements(page=page, title=await program_title(title="⚙️ Настройки"),
                             buttons=[
                                 await create_buttons(text="🔗 Подключение прокси", on_click=connection_proxy),
                                 await create_buttons(text="⏳ Запись времени", on_click=record_time),
                                 await create_buttons(text="🆔 Запись ID и Hash", on_click=record_id_hash),
                                 await create_buttons(text="✉️ Запись сообщения", on_click=recording_message),
                                 await create_buttons(text="⬅️ Назад", on_click=lambda _: page.go("/"))
                             ],
                             route_page="change_name_description_photo",
                             lv=lv)
    page.update()  # Обновляем страницу


async def handle_channel_subscription(page: ft.Page):
    """Создает страницу Подписка на каналы"""
    logger.info("Пользователь перешел на страницу Подписка на каналы")
    page.views.clear()  # Очищаем страницу и добавляем новый View
    lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
    page.controls.append(lv)  # добавляем ListView на страницу для отображения информации

    async def action_1(_):
        lv.controls.append(ft.Text("Подписка на каналы / группы"))  # отображаем сообщение в ListView
        page.update()  # Обновляем страницу
        client = await connect_telegram_account()

        channel_name = await read_channel_list_from_database()
        lv.controls.append(
            ft.Text(f"Группы и каналы из базы данных {channel_name}"))  # отображаем сообщение в ListView
        page.update()  # Обновляем страницу
        for channel in channel_name:
            lv.controls.append(ft.Text(f"Подписка на: {channel[0]}"))  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
            await SUBSCRIBE().subscribe_to_channel(client, channel[0], page, lv)
        lv.controls.append(ft.Text(f"Подписка завершена"))  # отображаем сообщение в ListView
        page.update()  # Обновляем страницу

    await view_with_elements(page=page, title=await program_title(title="Подписка на каналы"),
                             buttons=[
                                 await create_buttons(text="Подписка", on_click=action_1),
                                 await create_buttons(text="Назад", on_click=lambda _: page.go("/"))
                             ],
                             route_page="channel_subscription", lv=lv)
    page.update()  # Обновляем страницу


async def handle_creating_list_of_channels(page: ft.Page):
    """Создает страницу 📂 Формирование списка каналов"""
    logger.info("Пользователь перешел на страницу Формирование списка каналов")
    page.views.clear()  # Очищаем страницу и добавляем новый View
    lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
    page.controls.append(lv)  # добавляем ListView на страницу для отображения информации

    list_of_channels = ft.TextField(label="Введите список каналов", multiline=True, max_lines=19)

    async def action_1(_):
        try:
            lv.controls.append(
                ft.Text("📝 Запись данных, введенных пользователем..."))  # отображаем сообщение в ListView
            lv.controls.append(ft.Text(
                f"📋 Пользователь ввел список каналов: {list_of_channels.value}"))  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
            # Вызываем функцию для сохранения данных в базу данных
            await save_channels_to_db(list_of_channels.value)
            lv.controls.append(
                ft.Text("✅ Данные успешно записаны в базу данных!"))  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
        except Exception as e:
            logger.error(e)
            lv.controls.append(ft.Text(f"❌ Ошибка: {str(e)}"))  # отображаем ошибку в ListView
            page.update()  # Обновляем страницу

    await view_with_elements_input_field(page=page,
                                         title=await program_title(title="📂 Формирование списка каналов"),
                                         buttons=[
                                             await create_buttons(text="✅ Готово", on_click=action_1),
                                             await create_buttons(text="Назад", on_click=lambda _: page.go("/"))
                                         ],
                                         route_page="creating_list_of_channels",
                                         lv=lv,
                                         text_field=list_of_channels  # Создаем TextField поле ввода
                                         )
    page.update()  # Обновляем страницу


async def handle_documentation(page: ft.Page):
    """
    Создает страницу документации.

    При запуске функции автоматически открывается файл `doc/doc.md`,
    который содержит документацию по использованию программы.
    Также добавлена кнопка "Назад" для возврата в начальное меню.

    :param page: Страница приложения.
    """
    logger.info("Пользователь перешел на страницу документации")

    # Очищаем страницу и настраиваем шрифты
    page.views.clear()
    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",  # Шрифт
    }
    page.scroll = "auto"

    # Функция для загрузки и отображения Markdown-файла
    def load_markdown(file_path: str):
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                markdown_content = f.read()
            return markdown_content
        except FileNotFoundError:
            return "Файл документации не найден."
        except Exception as e:
            return f"Ошибка при чтении файла: {str(e)}"

    # Загружаем файл документации
    markdown_content = load_markdown("doc/doc.md")
    # Создаем Markdown-виджет для отображения документации
    markdown_widget = ft.Markdown(
        markdown_content,
        selectable=True,
        code_style=ft.TextStyle(font_family="Roboto Mono"),
        on_tap_link=lambda e: page.launch_url(e.data),  # Открываем ссылки в браузере
    )

    async def open_website(_):
        """Открывает веб-версию документации"""
        page.launch_url("https://github.com/pyadrus/TelegramMaster_Commentator/blob/master/doc/doc.md")

    # Добавляем элементы на страницу
    await view_with_elements(page=page,
                             title=await program_title(title="Документация"),  # Создаем заголовок страницы
                             buttons=[
                                 await create_buttons(text="🌐 Открыть сайт", on_click=open_website),
                                 await create_buttons(text="Назад", on_click=lambda _: page.go("/"))
                             ],
                             route_page="documentation",
                             lv=ft.ListView(controls=[markdown_widget], expand=True, spacing=10, padding=20),
                             )

    # Обновляем страницу
    page.update()
