import flet as ft
from faker import Faker
from telethon import functions
from loguru import logger

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
