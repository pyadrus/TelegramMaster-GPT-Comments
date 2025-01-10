from faker import Faker
from telethon import functions
import flet as ft

from src.core.commentator import log_messagess

about = "Мой основной проект https://t.me/+UvdDWG8iGgg1ZWUy"


async def change_profile_descriptions(client, text_field: ft.TextField) -> None:
    """
    Обновляет описание профиля Telegram со случайными данными.

    :param client: TelegramClient объект.
    :return: None
    """
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    log_messagess(f"{fake_name}", text_field)  # Сообщаем об успехе
    # Вводим данные для телеги
    with client as client:
        result = client(functions.account.UpdateProfileRequest(about=about))
        log_messagess(f"{result}", text_field)  # Сообщаем об успехе
        log_messagess("Профиль успешно обновлен!", text_field)  # Сообщаем об успехе
