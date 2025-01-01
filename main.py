import configparser
import datetime
import time
import telethon
from faker import Faker
from loguru import logger
from rich import print
from rich.progress import track
from telethon import functions
from telethon.sync import TelegramClient
from app_banner import banner
from working_with_the_database import reading_from_the_channel_list_database, creating_a_channel_list

logger.add("logs/log.log", format="{time} {level} {message}")


def read_config():
    """Считывание данных с config файла"""
    config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
    config.read("setting/config.ini")
    return config


def connect_telegram_account(api_id, api_hash):
    """Подключение к аккаунту Telegram"""
    client = TelegramClient('accounts/session_name', api_id, api_hash)
    client.connect()
    return client


class TelegramCommentator:
    """Инициализация комментатора Telegram"""

    def __init__(self, config) -> None:
        self.config = config
        self.client = None

    def subscribe_to_channel(self, channel_name):
        try:
            channel_entity = self.client.get_entity(channel_name)
            self.client.send_message(entity=channel_entity, message='/subscribe')  # Отправить команду на подписку
            logger.info(f'Подписка на канал {channel_name} выполнена успешно.')
        except Exception as e:
            logger.exception(f'Ошибка при подписке на канал {channel_name}')

    def write_comments_in_telegram(self, channels) -> None:
        """Пишите комментарии в Telegram-каналах"""
        last_message_ids = {name: 0 for name in channels}
        for name in channels:
            # Подписываемся на канал перед отправкой комментария
            self.subscribe_to_channel(name)
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

    def start_telegram_client(self) -> None:
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))

    def run(self, channels) -> None:
        self.start_telegram_client()
        while True:
            self.write_comments_in_telegram(channels)


def main(client):
    """Получаем список диалогов (каналов, групп и т. д.)"""
    dialogs = client.get_dialogs()

    creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite

    client.disconnect()  # Завершаем работу клиента


def change_profile_descriptions(client):
    """Смена описания профиля"""
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    logger.info(fake_name)
    # Вводим данные для телеги
    with client as client:
        about = "Мой основной проект https://t.me/+UvdDWG8iGgg1ZWUy"
        result = client(functions.account.UpdateProfileRequest(about=about))
        logger.info(result)
        logger.info("Профиль успешно обновлен!")


if __name__ == "__main__":
    logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы
    config = read_config()
    banner()
    print("[bold red][1] - Получение списка каналов")
    print("[bold red][2] - Отправка комментариев")
    print("[bold red][3] - Смена: имени, описания, фото профиля\n")
    user_input = input("Ваш выбор: ")
    if user_input == "1":
        client = connect_telegram_account(config.get("telegram_settings", "id"),
                                          config.get("telegram_settings", "hash"))
        main(client)
    elif user_input == "2":
        try:
            results = reading_from_the_channel_list_database()
            usernames = [row[0] for row in results]  # Преобразуем результат в словарь
            logger.info(usernames)  # Выводим полученный словарь
            telegram_commentator = TelegramCommentator(config)  # Каналы с комментариями
            telegram_commentator.run(usernames)
        except Exception as e:
            logger.exception(e)
            logger.info("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
    elif user_input == "3":
        client = connect_telegram_account(config.get("telegram_settings", "id"),
                                          config.get("telegram_settings", "hash"))
        change_profile_descriptions(client)
