import configparser
import datetime
import sqlite3
import time

import openai
import telethon
from faker import Faker
from loguru import logger
from rich.progress import track
from telethon import functions
from telethon.sync import TelegramClient


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
        openai_api_key = self.config.get("openai_api_key", "openai_api_key")
        openai.api_key = openai_api_key  # ChatGPT токен
        self.client = None

    def subscribe_to_channel(self, channel_name):
        try:
            channel_entity = self.client.get_entity(channel_name)
            self.client.send_message(entity=channel_entity, message='/subscribe')  # Отправить команду на подписку
            print(f'Подписка на канал {channel_name} выполнена успешно.')
        except Exception as e:
            print(f'Ошибка при подписке на канал {channel_name}: {e}')

    def write_comments_in_telegram(self, channels) -> None:
        """Пишите комментарии в Telegram-каналах"""
        last_message_ids = {name: 0 for name in channels}
        for name in channels:
            # Подписываемся на канал перед отправкой комментария
            self.subscribe_to_channel(name)
            try:
                channel_entity = self.client.get_entity(name)
                messages = self.client.get_messages(channel_entity, limit=1)
                print(messages)
                if messages:
                    for post in messages:
                        if post.id != last_message_ids[name]:
                            last_message_ids[name] = post.id
                            prompt = ("Вы патриотичный человек Российской Федерации. Напишите содержательный и"
                                      "яркий комментарий менее чем в 11 словах к следующему посту:") + post.raw_text
                            try:
                                output = openai.Completion.create(engine='text-davinci-003', prompt=prompt,
                                                                  max_tokens=170,
                                                                  temperature=0.4, n=1, stop=None)
                                if output.choices:
                                    output = output.choices[0].text.strip()
                                    if output == "":
                                        output = "Не знаю, что сказать..."
                                else:
                                    output = "Не знаю, что сказать..."
                                try:
                                    self.client.send_message(entity=name, message=output, comment_to=post.id)
                                    print(f'Наш комментарий: {output}')
                                    for i in track(range(400), description="Перерыв в рассылке..."):
                                        time.sleep(1)
                                except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                                    print(f"Вы не можете отправлять сообщения в: {name}")
                                except telethon.errors.rpcerrorlist.MsgIdInvalidError:
                                    print("Возможно пост был изменен или удален")
                                except telethon.errors.rpcerrorlist.UserBannedInChannelError:
                                    print("Вам запрещено отправлять сообщения в супергруппы/каналы (вызвано SendMessageRequest)")
                                except telethon.errors.rpcerrorlist.FloodWaitError as e:
                                    print(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}')
                                    time.sleep(e.seconds)
                                except telethon.errors.rpcerrorlist.ChatGuestSendForbiddenError as e:
                                    print(e)
                            except openai.error.RateLimitError:
                                print("Достигнут предел скорости для default-text-davinci-003 по количеству запросов в минуту. Ограничение: 3/мин. Пожалуйста, повторите попытку через 20 секунд. ")
                                time.sleep(200)
                            except openai.error.APIConnectionError:
                                print("Возникла проблема при попытке связаться с API OpenAI")
                                break
            except telethon.errors.rpcerrorlist.FloodWaitError as e:  # Если ошибка при подписке
                print(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}')
                time.sleep(e.seconds)
            except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError:  # Если аккаунт заблочен
                print("Аккаунт заблокирован")
                break

    def start_telegram_client(self) -> None:
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))

    def run(self, channels) -> None:
        self.start_telegram_client()
        while True:
            self.write_comments_in_telegram(channels)


# Путь к файлу базы данных SQLite
db_path = 'channels.db'


def main(client):
    # Получаем список диалогов (каналов, групп и т. д.)
    dialogs = client.get_dialogs()
    # Создаем или подключаемся к базе данных SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Создаем таблицу для хранения каналов, если ее еще нет
    cursor.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, title TEXT, username TEXT)''')
    # Проходим по диалогам и записываем информацию о каналах в базу данных
    for dialog in dialogs:
        if dialog.is_channel:
            title = dialog.title
            username = dialog.entity.username if dialog.entity.username else ''
            print(username)
            # Вставляем данные в базу данных
            cursor.execute('INSERT INTO channels (title, username) VALUES (?, ?)', (title, username))
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    # Завершаем работу клиента
    client.disconnect()


def change_profile_descriptions(client):
    """Смена описания профиля"""
    fake = Faker('ru_RU')  # Устанавливаем локаль для генерации русских имен
    fake_name = fake.first_name_female()  # Генерируем женское имя
    print(fake_name)
    # Вводим данные для телеги
    with client as client:
        about = "Мой основной проект https://t.me/+cKV31TBpVK85ZTAy"
        # result = client(functions.account.UpdateProfileRequest(first_name=fake_name, last_name='', about=about))
        result = client(functions.account.UpdateProfileRequest(about=about))
        print(result)
        print("Профиль успешно обновлен!")


if __name__ == "__main__":
    logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы
    config = read_config()
    print("[1] - Получение списка каналов")
    print("[2] - Отправка комментариев")
    print("[3] - Смена: имени, описания, фото профиля")
    user_input = input("Ваш выбор: ")
    if user_input == "1":
        client = connect_telegram_account(config.get("telegram_settings", "id"),
                                          config.get("telegram_settings", "hash"))
        main(client)
    elif user_input == "2":
        try:
            db_path = 'channels.db'  # Путь к файлу базы данных SQLite
            conn = sqlite3.connect(db_path)  # Создаем подключение к базе данных
            cursor = conn.cursor()
            # Выполняем SQL-запрос для извлечения username из таблицы channels
            cursor.execute('SELECT username FROM channels')
            results = cursor.fetchall()  # Получаем все строки результата запроса
            conn.close()  # Закрываем соединение с базой данных
            usernames = [row[0] for row in results]  # Преобразуем результат в словарь
            print(usernames)  # Выводим полученный словарь
            telegram_commentator = TelegramCommentator(config)  # Каналы с комментариями
            telegram_commentator.run(usernames)
        except Exception as e:
            logger.exception(e)
            print("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
    elif user_input == "3":
        client = connect_telegram_account(config.get("telegram_settings", "id"),
                                          config.get("telegram_settings", "hash"))
        change_profile_descriptions(client)
