import sqlite3

# Путь к файлу базы данных SQLite
db_path = 'channels.db'


async def save_channels_to_db(channels_data: str):
    """
    Сохраняет список каналов, введенный пользователем, в базу данных SQLite.

    :param channels_data: Строка с данными, введенными пользователем (список каналов).
    :return: None
    """
    # Разделяем введенные данные на отдельные каналы (предполагаем, что каналы разделены запятыми или переносами строк)
    channels_list = [channel.strip() for channel in channels_data.split(",")]  # Разделитель - запятая
    # Если каналы вводятся через перенос строки, можно использовать:
    # channels_list = [channel.strip() for channel in channels_data.split("\n")]

    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу для хранения информации о каналах, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_channels (
                        id INTEGER PRIMARY KEY,
                        channel_name TEXT
                    )''')

    # Записываем каждый канал в базу данных
    for channel in channels_list:
        if channel:  # Проверяем, что строка не пустая
            cursor.execute('INSERT INTO user_channels (channel_name) VALUES (?)', (channel,))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


async def creating_a_channel_list(dialogs):
    """
    Создает список каналов на основе переданных диалогов и записывает их в базу данных SQLite.

    :param dialogs: Список диалогов, содержащий объекты каналов.
    :return: Список имен пользователей (username) всех каналов.
    """

    username_diclist = []
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Создаем таблицу для хранения информации о каналах, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, title TEXT, username TEXT)''')
    # Проходим по диалогам и записываем информацию о каналах в базу данных
    for dialog in dialogs:
        if dialog.is_channel:
            title = dialog.title
            username = dialog.entity.username if dialog.entity.username else ''
            username_diclist.append(username)
            # Вставляем данные в базу данных
            cursor.execute('INSERT INTO channels (title, username) VALUES (?, ?)', (title, username))
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

    return username_diclist


async def reading_from_the_channel_list_database():
    """
    Считывает список имен пользователей (username) каналов из базы данных SQLite.

    :return: Список кортежей с именами пользователей каналов.
    """
    conn = sqlite3.connect(db_path)  # Создаем подключение к базе данных
    cursor = conn.cursor()
    # Выполняем SQL-запрос для извлечения username из таблицы channels
    cursor.execute('SELECT username FROM channels')
    results = cursor.fetchall()  # Получаем все строки результата запроса
    conn.close()  # Закрываем соединение с базой данных
    return results


async def read_channel_list_from_database():
    """
    Считывает список каналов из базы данных SQLite.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_name FROM user_channels')
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    reading_from_the_channel_list_database()
