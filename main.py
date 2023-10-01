import configparser
import sqlite3
import time
import openai
from loguru import logger
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

    def write_comments_in_telegram(self, channels) -> None:
        """Пишите комментарии в Telegram-каналах"""
        last_message_ids = {name: 0 for name in channels}

        for name in channels:
            try:
                channel_entity = self.client.get_entity(name)
            except ValueError:
                print("Ошибка, пожалуйста, проверьте свои сообщения!")
                continue

            messages = self.client.get_messages(channel_entity, limit=1)
            print(messages)
            if messages:
                for post in messages:
                    if post.id != last_message_ids[name]:
                        last_message_ids[name] = post.id
                        prompt = "Вы патриотичный человек Росийской Федерации и женщина. Напишите содержательный и яркий комментарий менее чем в 11 словах к следующему посту:" + post.raw_text
                        output = openai.Completion.create(engine='text-davinci-003', prompt=prompt, max_tokens=170,
                                                          temperature=0.4, n=1, stop=None)
                        if output.choices:
                            output = output.choices[0].text.strip()
                            if output == "":
                                output = "Не знаю, что сказать..."
                        else:
                            output = "Не знаю, что сказать..."
                        try:
                            time.sleep(25)
                            self.client.send_message(entity=name, message=output, comment_to=post.id)
                            self.client.send_message(f'{self.owner_id}',
                                                     f'Комментарий отправлен!\nОпубликовать ссылку: <a href="https://t.me/{name}/{post.id}">{name}</a>\nPost: {post.raw_text[:90]}\nНаш комментарий: {output}',
                                                     parse_mode="html")
                            print('Комментарий успешно отправлен, пожалуйста, проверьте свои сообщения')
                        except Exception:
                            print('Ошибка, пожалуйста, проверьте свои сообщения')
                            continue
                        finally:
                            time.sleep(25)

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
    # Авторизуемся в Telegram
    # client.start()
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


if __name__ == "__main__":
    logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы
    config = read_config()
    print("[1] - Получение списка каналов")
    print("[2] - Отправка комментариев")
    user_input = input("Ваш выбор: ")
    if user_input == "1":
        client = connect_telegram_account(config.get("telegram_settings", "id"),
                                          config.get("telegram_settings", "hash"))
        main(client)
    elif user_input == "2":
        try:
            # Каналы с комментариями
            channels = ['energynewz', 'militaryZmediaa', 'novosti_ru_24', 'voenacher', 'rusich_army',
                        'RVvoenkor', 'donbass_medi', 'boris_rozhin', 'readovkanews', 'osetin20', 'rusich_army']
            telegram_commentator = TelegramCommentator(config)
            telegram_commentator.run(channels)
        except Exception as e:
            logger.exception(e)
            print("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
