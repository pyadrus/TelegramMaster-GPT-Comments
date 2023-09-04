from telethon.sync import TelegramClient
import openai
import os
import time
import configparser

def read_config():
    """Считывание данных с config файла"""
    config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
    config.read("setting/config.ini")
    return config


def connect_telegram_account(api_id, api_hash):
    """Подключение к аккаунту Telegram"""
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()
    return client


class TelegramCommentator:
    """Инициализация комментатора Telegram"""
    def __init__(self, config):
        self.config = config
        openai.api_key = os.getenv("OpenAI_token")  # ChatGPT токен
        self.owner_id = os.getenv('Owner_id')
        self.client = None

    # Write comments in Telegram channels
    def write_comments_in_telegram(self, channels):
        last_message_ids = {name: 0 for name in channels}

        for name in channels:
            try:
                channel_entity = self.client.get_entity(name)
            except ValueError as e:
                self.client.send_message(f'{self.owner_id}', f"Ошибка получения информации о канале '{name}': {e}")
                print("Ошибка, пожалуйста, проверьте свои сообщения!")
                continue

            messages = self.client.get_messages(channel_entity, limit=1)
            if messages:
                for post in messages:
                    if post.id != last_message_ids[name]:
                        last_message_ids[name] = post.id

                        prompt = "Вы патриотичный человек и женщина. Напишите содержательный и яркий комментарий менее чем в 11 словах к следующему посту:" + post.raw_text
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
                        except Exception as e:
                            self.client.send_message(f'{self.owner_id}',
                                                     f"Ошибка отправки комментария на канал.'{name}': {e}")
                            print('Ошибка, пожалуйста, проверьте свои сообщения')
                        finally:
                            time.sleep(25)

    def start_telegram_client(self):
        self.client = connect_telegram_account(self.config.get("telegram_settings", "id"),
                                               self.config.get("telegram_settings", "hash"))

    def run(self, channels):
        self.start_telegram_client()
        while True:
            self.write_comments_in_telegram(channels)


# Main program
if __name__ == "__main__":
    config = read_config()
    channels = ['energynewz', 'militaryZmediaa', 'novosti_ru_24', 'voenacher']
    telegram_commentator = TelegramCommentator(config)
    telegram_commentator.run(channels)
