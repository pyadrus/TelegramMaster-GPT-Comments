import sqlite3

# Путь к файлу базы данных SQLite
db_path = 'channels.db'


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


if __name__ == "__main__":
    reading_from_the_channel_list_database()
