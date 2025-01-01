import datetime
import time
import tkinter as tk

import telethon
from faker import Faker
from loguru import logger
from rich import print
from rich.progress import track
from telethon import functions
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from config.config_handler import read_config
from working_with_the_database import reading_from_the_channel_list_database, creating_a_channel_list

logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы
about = "Мой основной проект https://t.me/+UvdDWG8iGgg1ZWUy"


def connect_telegram_account(api_id, api_hash) -> TelegramClient:
    """
    Подключается к Telegram аккаунту используя api_id и api_hash.

    :param api_id: Идентификатор API Telegram.
    :param api_hash: Ключ API Telegram.
    :return: TelegramClient объект, подключенный к Telegram.
    """
    client = TelegramClient('accounts/session_name', api_id, api_hash)
    client.connect()
    return client


class TelegramCommentator:
    """
    Класс для автоматизированной работы с комментариями в Telegram-каналах.

    :param config: Объект configparser.ConfigParser, содержащий настройки.
    """

    def __init__(self, config) -> None:
        self.config = config
        self.client = None

    def subscribe_to_channel(self, client, channel_name) -> None:
        """
        Подписывается на Telegram-канал.

        :param channel_name: Имя канала Telegram.
        :param client: TelegramClient объект.
        """
        try:
            client(JoinChannelRequest(channel_name))
            logger.info(f'Подписка на канал {channel_name} выполнена успешно.')
        except Exception as e:
            logger.exception(f'Ошибка при подписке на канал {channel_name}')

    def write_comments_in_telegram(self, client, channels) -> None:
        """
        Пишет комментарии в указанных Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        :param client: TelegramClient объект.
        """
        last_message_ids = {name: 0 for name in channels}
        for name in channels:

            self.subscribe_to_channel(client, channel_name=name)  # Подписываемся на канал перед отправкой комментария
            try:
                channel_entity = self.client.get_entity(name)
                messages = self.client.get_messages(channel_entity, limit=1)
                for message in messages:
                    logger.info(
                        f"ID сообщения: {message.id} ID: {message.peer_id} Дата: {message.date} Сообщение: {message.message}")

                    if messages:
                        post = messages[0]
                        if post.id != last_message_ids.get(name, None):
                            last_message_ids[name] = post.id
                            message = 'Россия лучшая страна!'
                            try:
                                self.client.send_message(entity=name, message=message, comment_to=post.id)
                                logger.info(f'Наш комментарий: {message}')
                                for i in track(range(400), description="Перерыв в рассылке..."):
                                    time.sleep(1)
                            except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                                logger.info(f"Вы не можете отправлять сообщения в: {name}")
                            except telethon.errors.rpcerrorlist.MsgIdInvalidError:
                                logger.info("Возможно пост был изменен или удален")
                            except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                                logger.info("Вам запрещено отправлять сообщения в супергруппы/каналы "
                                            "(вызвано SendMessageRequest)")
                            except telethon.errors.rpcerrorlist.FloodWaitError as e:
                                logger.info(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}')
                                time.sleep(e.seconds)
                            except telethon.errors.rpcerrorlist.ChatGuestSendForbiddenError as e:
                                logger.info(e)
                            except telethon.errors.rpcerrorlist.ChannelPrivateError:
                                logger.info(f"Канал {name} закрыт")
            except telethon.errors.rpcerrorlist.FloodWaitError as e:  # Если ошибка при подписке
                logger.info(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}')
                time.sleep(e.seconds)
            except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError:  # Если аккаунт заблочен
                logger.info("Аккаунт заблокирован")
                break

    def run(self, channels) -> None:
        """
        Запускает процесс комментирования в Telegram-каналах.

        :param channels: Список имен Telegram-каналов.
        """
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))
        while True:
            self.write_comments_in_telegram(self.client, channels)


def main(client) -> None:
    """
    Получает список диалогов (каналов, групп и т. д.) и создаёт базу данных.

    :param client: TelegramClient объект.
    """
    dialogs = client.get_dialogs()
    creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite
    client.disconnect()  # Завершаем работу клиента


def change_profile_descriptions(client) -> None:
    """
    Обновляет описание профиля Telegram со случайными данными.

    :param client: TelegramClient объект.
    """
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    logger.info(fake_name)
    # Вводим данные для телеги
    with client as client:
        result = client(functions.account.UpdateProfileRequest(about=about))
        logger.info(result)
        logger.info("Профиль успешно обновлен!")


def action_1():
    print("[bold red]Получение списка каналов")
    config = read_config()
    client = connect_telegram_account(config.get("telegram_settings", "id"),
                                      config.get("telegram_settings", "hash"))
    main(client)


def action_2():
    print("[bold red]Отправка комментариев")
    try:
        config = read_config()
        results = reading_from_the_channel_list_database()
        usernames = [row[0] for row in results]  # Преобразуем результат в словарь
        logger.info(usernames)  # Выводим полученный словарь
        telegram_commentator = TelegramCommentator(config)  # Каналы с комментариями
        telegram_commentator.run(usernames)
    except Exception as e:
        logger.exception(e)
        logger.info("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")


def action_3():
    print("[bold red]Смена: имени, описания, фото профиля")
    config = read_config()
    client = connect_telegram_account(config.get("telegram_settings", "id"),
                                      config.get("telegram_settings", "hash"))
    change_profile_descriptions(client)


if __name__ == "__main__":
    # Создаем главное окно
    root = tk.Tk()
    program_version, date_of_program_change = "0.0.4", "01.01.2025"  # Версия программы, дата изменения
    root.title(f"Версия {program_version}. Дата изменения {date_of_program_change}")  # Описание окна
    root.geometry("400x200")  # Размер окна ширина, высота

    # Создаем кнопки
    btn_1 = tk.Button(root, text="Получение списка каналов", command=action_1)
    btn_1.pack(pady=10)
    btn_2 = tk.Button(root, text="Отправка комментариев", command=action_2)
    btn_2.pack(pady=10)
    btn_3 = tk.Button(root, text="Смена имени, описания, фото", command=action_3)
    btn_3.pack(pady=10)

    # Запускаем главный цикл приложения
    root.mainloop()
