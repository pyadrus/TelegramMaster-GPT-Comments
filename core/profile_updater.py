import tkinter as tk

from faker import Faker
# from loguru import logger
from telethon import functions

from gui.log_message import log_message

about = "Мой основной проект https://t.me/+UvdDWG8iGgg1ZWUy"


def change_profile_descriptions(client, text_widget: tk.Text) -> None:
    """
    Обновляет описание профиля Telegram со случайными данными.

    :param client: TelegramClient объект.
    :param text_widget: Текстовое поле для вывода сообщений.
    :return: None
    """
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    log_message(f"{fake_name}", text_widget)  # Сообщаем об успехе
    # Вводим данные для телеги
    with client as client:
        result = client(functions.account.UpdateProfileRequest(about=about))
        log_message(f"{result}", text_widget)  # Сообщаем об успехе
        log_message("Профиль успешно обновлен!", text_widget)  # Сообщаем об успехе
