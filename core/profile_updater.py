from faker import Faker
from loguru import logger
from telethon import functions

about = "Мой основной проект https://t.me/+UvdDWG8iGgg1ZWUy"


def change_profile_descriptions(client) -> None:
    """
    Обновляет описание профиля Telegram со случайными данными.

    :param client: TelegramClient объект.
    :return: None
    """
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    logger.info(fake_name)
    # Вводим данные для телеги
    with client as client:
        result = client(functions.account.UpdateProfileRequest(about=about))
        logger.info(result)
        logger.info("Профиль успешно обновлен!")
