import sqlite3

# Путь к файлу базы данных SQLite
db_path = '../channels.db'


def creating_a_channel_list(dialogs):
    """Создание списка каналов"""

    username_diclist = []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Создаем таблицу для хранения каналов, если ее еще нет
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


def reading_from_the_channel_list_database():
    """Считывание списка каналов с базы данных"""
    conn = sqlite3.connect(db_path)  # Создаем подключение к базе данных
    cursor = conn.cursor()
    # Выполняем SQL-запрос для извлечения username из таблицы channels
    cursor.execute('SELECT username FROM channels')
    results = cursor.fetchall()  # Получаем все строки результата запроса
    conn.close()  # Закрываем соединение с базой данных
    return results


if __name__ == "__main__":
    reading_from_the_channel_list_database()
