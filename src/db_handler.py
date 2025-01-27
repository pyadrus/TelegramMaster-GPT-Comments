# -*- coding: utf-8 -*-
import sqlite3

from loguru import logger
from peewee import SqliteDatabase

# Путь к файлу базы данных SQLite
db_path = 'data/database/app.db'
db = SqliteDatabase('data/database/app.db')


async def save_channels_to_db(channels_data: str):
    """
    Сохраняет список каналов, введенный пользователем, в базу данных SQLite.

    :param channels_data: Строка с данными, введенными пользователем (список каналов).
    :return: None
    """
    # Разделяем введенные данные на отдельные каналы (предполагаем, что каналы разделены запятыми или переносами строк)
    channels_list = [channel.strip() for channel in channels_data.split(",")]  # Разделитель - запятая
    # Если каналы вводятся через перенос строки, можно использовать:

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


class DatabaseHandler:

    def __init__(self, db_file="data/database/app.db"):
        self.db_file = db_file

    async def connect(self) -> None:
        """Подключение к базе данных"""
        self.sqlite_connection = sqlite3.connect(self.db_file)
        self.cursor = self.sqlite_connection.cursor()

    def close(self) -> None:
        """Закрытие соединения с базой данных"""
        self.sqlite_connection.close()

    async def open_and_read_data(self, table_name) -> list:
        """
        Открываем базу и считываем данные из указанной таблицы

        :param table_name: Название таблицы, данные из которой требуется извлечь.
        :return: Список записей из таблицы

        В случае ошибок базы данных (например, поврежденный файл базы данных или некорректный запрос)
        метод ловит исключения типа `sqlite3.Error` и записывает ошибку в лог, но не выбрасывает её дальше.
        Это предотвращает аварийное завершение работы программы и позволяет продолжить выполнение.
        """
        try:
            await self.connect()
            self.cursor.execute(f"SELECT * FROM {table_name}")
            records = self.cursor.fetchall()
            self.close()
            return records
        except sqlite3.DatabaseError as error:  # Ошибка при открытии базы данных
            logger.error(f"❌ Ошибка при открытии базы данных, возможно база данных повреждена: {error}")
            return []
        except sqlite3.Error as error:  # Ошибка при открытии базы данных
            logger.error(f"❌ Ошибка при открытии базы данных: {error}")
            return []
        finally:
            self.close()  # Закрываем соединение

    async def deleting_an_invalid_proxy(self, proxy_type, addr, port, username, password, rdns) -> None:
        """
        Удаляем не рабочий proxy с software_database.db, таблица proxy

        :param proxy_type: тип proxy
        :param addr: адрес
        :param port: порт
        :param username: имя пользователя
        :param password: пароль
        :param rdns: прокси
        """
        await self.connect()
        self.cursor.execute(
            f"DELETE FROM proxy WHERE proxy_type='{proxy_type}' AND addr='{addr}' AND port='{port}' AND "
            f"username='{username}' AND password='{password}' AND rdns='{rdns}'"
        )
        logger.info(f"{self.cursor.rowcount} rows deleted")
        self.sqlite_connection.commit()  # cursor_members.commit() – применение всех изменений в таблицах БД
        self.close()  # cursor_members.close() – закрытие соединения с БД.

    async def save_proxy_data_to_db(self, proxy) -> None:
        """Запись данных proxy в базу данных"""
        await self.connect()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS proxy(proxy_type, addr, port, username, password, rdns)")
        self.cursor.executemany("INSERT INTO proxy(proxy_type, addr, port, username, password, rdns) "
                                "VALUES (?, ?, ?, ?, ?, ?)", (proxy,), )
        self.sqlite_connection.commit()
        self.close()  # cursor_members.close() – закрытие соединения с БД.


if __name__ == "__main__":
    reading_from_the_channel_list_database()
