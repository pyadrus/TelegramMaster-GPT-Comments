# -*- coding: utf-8 -*-
import flet as ft
from faker import Faker
from loguru import logger
from telethon import functions

from src.core.buttons import create_buttons
from src.core.views import view_with_elements, program_title
from src.telegram_client import connect_telegram_account


async def handle_change_name_description_photo(page: ft.Page):
    """Создает страницу 🖼️ Смена имени, описания"""
    logger.info("Пользователь перешел на страницу Смена имени, описания")
    page.views.clear()  # Очищаем страницу и добавляем новый View
    lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
    page.controls.append(lv)  # добавляем ListView на страницу для отображения информации

    async def action_1(_):
        try:
            lv.controls.append(ft.Text("🖼️ Смена имени, описания"))  # отображаем сообщение в ListView
            page.update()  # Обновляем страницу
            client = await connect_telegram_account()
            await change_profile_descriptions(client, lv)
            page.update()  # Обновляем страницу
        except Exception as e:
            logger.error(e)
            lv.controls.append(ft.Text(f"Ошибка: {str(e)}"))  # отображаем ошибку в ListView
            page.update()  # Обновляем страницу

    await view_with_elements(page=page, title=await program_title(title="🖼️ Смена имени, описания"),
                             buttons=[
                                 await create_buttons(text="🖼️ Смена имени, описания",
                                                      on_click=action_1),
                                 await create_buttons(text="Назад", on_click=lambda _: page.go("/"))
                             ],
                             route_page="change_name_description_photo",
                             lv=lv)
    page.update()  # Обновляем страницу


about = "Мой основной проект https://t.me/+UvdDWG8iGgg1ZWUy"


async def change_profile_descriptions(client, lv: ft.ListView) -> None:
    """
    Обновляет описание профиля Telegram и имя со случайными данными с помощью библиотеки Faker.

    :param client: TelegramClient объект.
    :param lv: ListView объект.
    :return: None
    """
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    lv.controls.append(ft.Text(f"🎭 Сгенерированное имя: {fake_name}"))  # отображаем сообщение в ListView

    # Вводим данные для телеги
    async with client:  # Используем асинхронный контекстный менеджер
        # Обновляем имя и описание профиля
        result = await client(
            functions.account.UpdateProfileRequest(
                first_name=fake_name,  # Устанавливаем новое имя
                about=about  # Устанавливаем новое описание
            )
        )
        logger.info(result)

        # Форматируем результат для пользователя
        user_info = (
            f"🆔 ID: {result.id}\n"
            f"👤 Имя: {result.first_name}\n"
            f"👥 Фамилия: {result.last_name}\n"
            f"📛 Username: {result.username}\n"
            f"📞 Телефон: {result.phone}\n"
            f"📝 Описание профиля обновлено: {about}"
        )

        # Добавляем отформатированные данные в ListView
        lv.controls.append(ft.Text(user_info))
        lv.controls.append(ft.Text("✅ Профиль успешно обновлен!"))  # отображаем сообщение в ListView
