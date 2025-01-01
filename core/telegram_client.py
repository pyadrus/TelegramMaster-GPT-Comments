from telethon.sync import TelegramClient


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
