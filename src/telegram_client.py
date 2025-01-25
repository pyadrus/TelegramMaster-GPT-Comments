from telethon.sync import TelegramClient

from src.config_handler import api_id, api_hash


async def connect_telegram_account() -> TelegramClient:
    """
    Подключается к Telegram аккаунту используя api_id и api_hash.

    :return: TelegramClient объект, подключенный к Telegram.
    """
    client = TelegramClient(
        'data/accounts/session_name',  # Путь и имя аккаунта.
        api_id,  # Идентификатор API Telegram.
        api_hash  # Ключ API Telegram.
    )

    await client.connect()
    return client


if __name__ == '__main__':
    connect_telegram_account()
