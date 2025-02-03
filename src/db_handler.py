# -*- coding: utf-8 -*-
import sqlite3

import aiosqlite
from loguru import logger

from src.config_handler import db_path


async def save_channels_to_db(channels_data: str, db_path: str = db_path) -> None:
    """
    Сохраняет список каналов, введенный пользователем, в базу данных SQLite.

    :param channels_data: Строка с данными, введенными пользователем (список каналов).
    :param db_path: Путь к файлу базы данных SQLite.
    :return: None
    """
    # Разделяем введенные данные на отдельные каналы
    # Учитываем запятые, пробелы и переносы строк
    channels_list = [
        channel.strip() for channel in channels_data.replace("\n", ",").split(",") if channel.strip()
    ]

    if not channels_list:
        logger.warning("❌ Список каналов пуст.")
        return

    try:
        # Подключаемся к базе данных асинхронно
        async with aiosqlite.connect(db_path) as conn:
            cursor = await conn.cursor()

            # Создаем таблицу для хранения информации о каналах, если она еще не существует
            await cursor.execute('''CREATE TABLE IF NOT EXISTS user_channels (
                                    id INTEGER PRIMARY KEY,
                                    channel_name TEXT UNIQUE
                                )''')

            # Записываем каждый канал в базу данных
            for channel in channels_list:
                try:
                    await cursor.execute(
                        'INSERT OR IGNORE INTO user_channels (channel_name) VALUES (?)', (channel,)
                    )
                except aiosqlite.Error as e:
                    logger.error(f"❌ Ошибка при добавлении канала {channel}: {e}")

            # Сохраняем изменения
            await conn.commit()
            logger.info(f"✅ Успешно сохранено {len(channels_list)} каналов.")
    except aiosqlite.Error as e:
        logger.error(f"❌ Ошибка при работе с базой данных: {e}")


async def creating_a_channel_list(dialogs):
    username_diclist = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS channels 
                    (id INTEGER PRIMARY KEY, title TEXT, username TEXT)''')

    # Удаляем записи с числовыми username
    cursor.execute("DELETE FROM channels WHERE username GLOB '[0-9]*'")

    for dialog in dialogs:
        if dialog.is_channel:
            title = dialog.title
            username = getattr(dialog.entity, 'username', '')

            # Пропускаем числовые username и пустые значения
            if username and not username.isdigit():
                username_diclist.append(username)
                cursor.execute('''
                    INSERT OR IGNORE INTO channels (title, username) 
                    VALUES (?, ?)
                ''', (title, username))

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
    read_channel_list_from_database()
