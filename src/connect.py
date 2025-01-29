# -*- coding: utf-8 -*-
import asyncio
import os
import os.path
import random
import shutil
import sqlite3

import flet as ft  # Импортируем библиотеку flet
import phonenumbers
import requests
from loguru import logger
from phonenumbers import carrier, geocoder
from telethon import TelegramClient
from telethon.errors import (AuthKeyDuplicatedError, PhoneNumberBannedError, UserDeactivatedBanError, TimedOutError,
                             AuthKeyNotFound, TypeNotFoundError, AuthKeyUnregisteredError, SessionPasswordNeededError,
                             ApiIdInvalidError, YouBlockedUserError)
from thefuzz import fuzz

from src.config_handler import api_id, api_hash, folder_accounts
from src.core.buttons import create_buttons
from src.core.notification import show_notification
from src.db_handler import DatabaseHandler
from src.logging_in import get_country_flag

# Наименование кнопок
back_button: str = "⬅️ Назад"
done_button: str = "✅ Готово"

height_button = 35
line_width_button = 850


def getting_phone_number_data_by_phone_number(phone_numbers):
    """
    Определение страны и оператора по номеру телефона

    :param phone_numbers: Номер телефона
    :return: None
    """

    # Пример номера телефона для анализа
    number = phonenumbers.parse(f"+{phone_numbers}", None)

    # Получение информации о стране и операторе на русском языке
    country_name = geocoder.description_for_number(number, "ru")
    operator_name = carrier.name_for_number(number, "ru")

    # Вывод информации
    logger.info(f"Номер: {phone_numbers}, Оператор: {operator_name}, Страна: {country_name}")


async def reading_proxy_data_from_the_database(db_handler):
    """
    Считываем данные для proxy c базы данных "software_database.db", таблица "proxy" где:
    proxy_type - тип proxy (например: SOCKS5), addr - адрес (например: 194.67.248.9), port - порт (например: 9795)
    username - логин (например: username), password - пароль (например: password)

    :param db_handler - объект класса DatabaseHandler
    """
    try:
        proxy_random_list = random.choice(await db_handler.open_and_read_data("proxy"))
        logger.info(f"{proxy_random_list}")
        proxy = {'proxy_type': (proxy_random_list[0]), 'addr': proxy_random_list[1], 'port': int(proxy_random_list[2]),
                 'username': proxy_random_list[3], 'password': proxy_random_list[4], 'rdns': proxy_random_list[5]}
        return proxy
    except IndexError:
        proxy = None
        return proxy
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


async def checking_the_proxy_for_work() -> None:
    """
    Проверка proxy на работоспособность с помощью Example.org. Example.org является примером адреса домена верхнего
    уровня, который используется для демонстрации работы сетевых протоколов. На этом сайте нет никакого контента, но он
    используется для различных тестов.
    """
    try:
        for proxy_dic in await DatabaseHandler().open_and_read_data("proxy"):
            logger.info(proxy_dic)
            # Подключение к proxy с проверкой на работоспособность
            await connecting_to_proxy_with_verification(proxy_type=proxy_dic[0],  # Тип proxy (например: SOCKS5)
                                                        addr=proxy_dic[1],  # Адрес (например: 194.67.248.9)
                                                        port=proxy_dic[2],  # Порт (например: 9795)
                                                        username=proxy_dic[3],  # Логин (например: username)
                                                        password=proxy_dic[4],  # Пароль (например: password)
                                                        rdns=proxy_dic[5],
                                                        db_handler=DatabaseHandler())
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


async def connecting_to_proxy_with_verification(proxy_type, addr, port, username, password, rdns, db_handler) -> None:
    """Подключение к proxy с проверкой на работоспособность где: proxy_type - тип proxy (например: SOCKS5),
    addr - адрес (например: 194.67.248.9), port - порт (например: 9795), username - логин (например: username),
    password - пароль (например: password)

    :param proxy_type: тип proxy (например: SOCKS5)
    :param addr: адрес (например: 194.67.248.9)
    :param port: порт (например: 9795)
    :param username: логин (например: username)
    :param password: пароль (например: password)
    :param rdns: rdns (например: rdns)
    :param db_handler: объект класса DatabaseHandler
    """
    # Пробуем подключиться по прокси
    try:
        # Указываем параметры прокси
        proxy = {'http': f'{proxy_type}://{username}:{password}@{addr}:{port}'}
        emoji, country = get_country_flag(addr)
        logger.info(
            f"Проверяемый прокси: {proxy_type}://{username}:{password}@{addr}:{port}. Страна proxy {country} {emoji}")
        requests.get('http://example.org', proxies=proxy)
        logger.info(f'⚠️ Proxy: {proxy_type}://{username}:{password}@{addr}:{port} рабочий!')
    # RequestException исключение возникает при ошибках, которые могут быть вызваны при запросе к веб-серверу.
    # Это может быть из-за недоступности сервера, ошибочного URL или других проблем с соединением.
    except requests.exceptions.RequestException:
        logger.info('❌ Proxy не рабочий!')
        await db_handler.deleting_an_invalid_proxy(proxy_type, addr, port, username, password, rdns)
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


def find_filess(directory_path, extension) -> list:
    """
    Поиск файлов с определенным расширением в директории. Расширение файла должно быть указанно без точки.

    :param directory_path: Путь к директории
    :param extension: Расширение файла (указанное без точки)
    :return list: Список имен найденных файлов
    """
    entities = []  # Создаем словарь с именами найденных аккаунтов в папке user_data/accounts
    try:
        for x in os.listdir(directory_path):
            if x.endswith(f".{extension}"):  # Проверяем, заканчивается ли имя файла на заданное расширение
                file = os.path.splitext(x)[0]  # Разделяем имя файла на имя без расширения и расширение
                entities.append(file)  # Добавляем информацию о файле в список

        logger.info(f"🔍 Найденные файлы: {entities}")  # Выводим имена найденных аккаунтов

        return entities  # Возвращаем список json файлов
    except FileNotFoundError:
        logger.error(f"❌ Ошибка! Директория {directory_path} не найдена!")


def working_with_accounts(account_folder, new_account_folder) -> None:
    """
    Работа с аккаунтами

    :param account_folder: Исходный путь к файлу
    :param new_account_folder: Путь к новой папке, куда нужно переместить файл
    """
    try:  # Переносим файлы в нужную папку
        os.replace(account_folder, new_account_folder)
    except FileNotFoundError:  # Если в папке нет нужной папки, то создаем ее
        try:
            os.makedirs(new_account_folder)
            os.replace(account_folder, new_account_folder)
        except FileExistsError:  # Если файл уже существует, то удаляем его
            os.remove(account_folder)
    except PermissionError as error:
        logger.error(f"❌ Ошибка: {error}")
        logger.error("❌ Не удалось перенести файлы в нужную папку")
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


class TGConnect:

    def __init__(self):
        self.db_handler = DatabaseHandler()

    async def verify_account(self, page: ft.Page, folder_name, session_name) -> None:
        """
        Проверяет и сортирует аккаунты.

        :param session_name: Имя аккаунта для проверки аккаунта
        :param folder_name: Папка с аккаунтами
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            logger.info(f"Проверка аккаунта {session_name}. Используем API ID: {api_id}, API Hash: {api_hash}")
            telegram_client = await self.get_telegram_client(page, session_name,
                                                             f"user_data/accounts/{folder_name}")
            try:
                await telegram_client.connect()  # Подсоединяемся к Telegram аккаунта
                if not await telegram_client.is_user_authorized():  # Если аккаунт не авторизирован
                    await telegram_client.disconnect()
                    await asyncio.sleep(5)
                    working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                                          f"user_data/accounts/banned/{session_name}.session")
                else:
                    logger.info(f'Аккаунт {session_name} авторизован')
                    await telegram_client.disconnect()  # Отключаемся после проверки
            except (PhoneNumberBannedError, UserDeactivatedBanError, AuthKeyNotFound,
                    AuthKeyUnregisteredError, AuthKeyDuplicatedError) as e:
                await self.handle_banned_account(telegram_client, folder_name, session_name, e)
            except TimedOutError as error:
                logger.exception(f"❌ Ошибка таймаута: {error}")
                await asyncio.sleep(2)
            except sqlite3.OperationalError:
                await telegram_client.disconnect()
                working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                                      f"user_data/accounts/banned/{session_name}.session")
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    @staticmethod
    async def handle_banned_account(telegram_client, folder_name, session_name, exception):
        """
        Обработка забаненных аккаунтов.
        telegram_client.disconnect() - Отключение от Telegram.
        working_with_accounts() - Перемещение файла. Исходный путь к файлу - account_folder. Путь к новой папке,
        куда нужно переместить файл - new_account_folder

        :param telegram_client: TelegramClient
        :param folder_name: Папка с аккаунтами
        :param session_name: Имя аккаунта
        :param exception: Расширение файла
        """
        logger.error(f"⛔ Аккаунт забанен: {session_name}. {str(exception)}")
        await telegram_client.disconnect()
        working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                              f"user_data/accounts/banned/{session_name}.session")

    async def check_for_spam(self, page: ft.Page, folder_name) -> None:
        """
        Проверка аккаунта на спам через @SpamBot

        :param folder_name: папка с аккаунтами
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            for session_name in find_filess(directory_path=f"user_data/accounts/{folder_name}",
                                            extension='session'):
                telegram_client = await self.get_telegram_client(page, session_name,
                                                                 account_directory=f"user_data/accounts/{folder_name}")
                try:
                    await telegram_client.send_message('SpamBot', '/start')  # Находим спам бот, и вводим команду /start
                    for message in await telegram_client.get_messages('SpamBot'):
                        logger.info(f"{session_name} {message.message}")
                        similarity_ratio_ru: int = fuzz.ratio(f"{message.message}",
                                                              "Очень жаль, что Вы с этим столкнулись. К сожалению, "
                                                              "иногда наша антиспам-система излишне сурово реагирует на "
                                                              "некоторые действия. Если Вы считаете, что Ваш аккаунт "
                                                              "ограничен по ошибке, пожалуйста, сообщите об этом нашим "
                                                              "модераторам. Пока действуют ограничения, Вы не сможете "
                                                              "писать тем, кто не сохранил Ваш номер в список контактов, "
                                                              "а также приглашать таких пользователей в группы или каналы. "
                                                              "Если пользователь написал Вам первым, Вы сможете ответить, "
                                                              "несмотря на ограничения.")
                        if similarity_ratio_ru >= 97:
                            logger.info('⛔ Аккаунт заблокирован')
                            await telegram_client.disconnect()  # Отключаемся от аккаунта, для освобождения процесса session файла.
                            logger.info(f"Проверка аккаунтов через SpamBot. {session_name}: {message.message}")
                            # Перенос Telegram аккаунта в папку banned, если Telegram аккаунт в бане
                            working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                                                  f"user_data/accounts/banned/{session_name}.session")
                        similarity_ratio_en: int = fuzz.ratio(f"{message.message}",
                                                              "I’m very sorry that you had to contact me. Unfortunately, "
                                                              "some account_actions can trigger a harsh response from our "
                                                              "anti-spam systems. If you think your account was limited by "
                                                              "mistake, you can submit a complaint to our moderators. While "
                                                              "the account is limited, you will not be able to send messages "
                                                              "to people who do not have your number in their phone contacts "
                                                              "or add them to groups and channels. Of course, when people "
                                                              "contact you first, you can always reply to them.")
                        if similarity_ratio_en >= 97:
                            logger.info('⛔ Аккаунт заблокирован')
                            await telegram_client.disconnect()  # Отключаемся от аккаунта, для освобождения процесса session файла.
                            logger.error(f"Проверка аккаунтов через SpamBot. {session_name}: {message.message}")
                            # Перенос Telegram аккаунта в папку banned, если Telegram аккаунт в бане
                            logger.info(session_name)
                            working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                                                  f"user_data/accounts/banned/{session_name}.session")
                        logger.error(f"Проверка аккаунтов через SpamBot. {session_name}: {message.message}")

                        try:
                            await telegram_client.disconnect()  # Отключаемся от аккаунта, для освобождения процесса session файла.
                        except sqlite3.OperationalError as e:
                            logger.info(f"Ошибка при отключении аккаунта: {session_name}")

                            await self.handle_banned_account(telegram_client, folder_name, session_name, e)

                except YouBlockedUserError:
                    continue  # Записываем ошибку в software_database.db и продолжаем работу
                except (AttributeError, AuthKeyUnregisteredError) as e:
                    logger.error(e)
                    continue

        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    async def verify_all_accounts(self, page: ft.Page, folder_name) -> None:
        """
        Проверяет все аккаунты Telegram в указанной директории.

        :param folder_name: Имя каталога с аккаунтами
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            logger.info(f"Запуск проверки аккаунтов Telegram из папки 📁: {folder_name}")
            await checking_the_proxy_for_work()  # Проверка proxy
            # Сканирование каталога с аккаунтами
            for session_file in find_filess(directory_path=f"user_data/accounts/{folder_name}",
                                            extension='session'):
                logger.info(f"⚠️ Проверяемый аккаунт: user_data/accounts/{session_file}")
                # Проверка аккаунтов
                await self.verify_account(page=page, folder_name=folder_name, session_name=session_file)
            logger.info(f"Окончание проверки аккаунтов Telegram из папки 📁: {folder_name}")
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    async def get_account_details(self, page: ft.Page, folder_name):
        """
        Получает информацию о Telegram аккаунте.

        :param folder_name: Имя каталога
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            logger.info(f"Запуск переименования аккаунтов Telegram из папки 📁: {folder_name}")
            await checking_the_proxy_for_work()  # Проверка proxy
            # Сканирование каталога с аккаунтами
            for session_name in find_filess(directory_path=f"user_data/accounts/{folder_name}",
                                            extension='session'):
                logger.info(f"⚠️ Переименовываемый аккаунт: user_data/accounts/{session_name}")
                # Переименовывание аккаунтов
                logger.info(
                    f"Переименовывание аккаунта {session_name}. Используем API ID: {api_id}, API Hash: {api_hash}")

                telegram_client = await self.get_telegram_client(page, session_name,
                                                                 account_directory=f"user_data/accounts/{folder_name}")

                try:
                    me = await telegram_client.get_me()
                    phone = me.phone
                    await self.rename_session_file(telegram_client, session_name, phone, folder_name)

                except AttributeError:  # Если в get_me приходит NoneType (None)
                    pass

                except TypeNotFoundError:
                    await telegram_client.disconnect()  # Разрываем соединение Telegram, для удаления session файла
                    logger.error(
                        f"⛔ Битый файл или аккаунт забанен: {session_name}.session. Возможно, запущен под другим IP")
                    working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                                          f"user_data/accounts/banned/{session_name}.session")
                except AuthKeyUnregisteredError:
                    await telegram_client.disconnect()  # Разрываем соединение Telegram, для удаления session файла
                    logger.error(
                        f"⛔ Битый файл или аккаунт забанен: {session_name}.session. Возможно, запущен под другим IP")
                    working_with_accounts(f"user_data/accounts/{folder_name}/{session_name}.session",
                                          f"user_data/accounts/banned/{session_name}.session")
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    @staticmethod
    async def rename_session_file(telegram_client, phone_old, phone, folder_name) -> None:
        """
        Переименовывает session файлы.

        :param telegram_client: Клиент для работы с Telegram
        :param phone_old: Номер телефона для переименования
        :param phone: Номер телефона для переименования (новое название для session файла)
        :param folder_name: Папка с аккаунтами
        """
        await telegram_client.disconnect()  # Отключаемся от аккаунта для освобождения session файла
        try:
            # Переименование session файла
            os.rename(f"user_data/accounts/{folder_name}/{phone_old}.session",
                      f"user_data/accounts/{folder_name}/{phone}.session", )
        except FileExistsError:
            # Если файл существует, то удаляем дубликат
            os.remove(f"user_data/accounts/{folder_name}/{phone_old}.session")
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

        getting_phone_number_data_by_phone_number(phone)  # Выводим информацию о номере телефона

    async def get_telegram_client(self, page, session_name, account_directory):
        """
        Подключение к Telegram, используя файл session.
        Имя файла сессии file[0] - session файл

        :param account_directory: Путь к директории
        :param session_name: Файл сессии (file[0] - session файл)
        :param page: Страница интерфейса Flet для отображения элементов управления.
        :return TelegramClient: TelegramClient
        """
        logger.info(
            f"Подключение к аккаунту: {account_directory}/{session_name}. Используем API ID: {api_id}, API Hash: {api_hash}")  # Имя файла сессии file[0] - session файл
        telegram_client = None  # Инициализируем переменную
        try:
            telegram_client = TelegramClient(f"{account_directory}/{session_name}", api_id=api_id,
                                             api_hash=api_hash,
                                             system_version="4.16.30-vxCUSTOM",
                                             proxy=await reading_proxy_data_from_the_database(self.db_handler))

            await telegram_client.connect()
            return telegram_client

        except sqlite3.OperationalError:

            logger.info(f"❌ Аккаунт {account_directory}/{session_name} поврежден.")
            await show_notification(
                page,
                f"⚠️ У нас возникла проблема с аккаунтом {account_directory}/{session_name}.\n\n"
                f"Чтобы избежать дальнейших ошибок, пожалуйста, удалите этот аккаунт вручную и попробуйте снова. 🔄"
            )

        except sqlite3.DatabaseError:

            logger.info(f"❌ Аккаунт {session_name} поврежден.")
            await show_notification(
                page,
                f"⚠️ У нас возникла проблема с аккаунтом {account_directory}/{session_name}.\n\n"
                f"Чтобы избежать дальнейших ошибок, пожалуйста, удалите этот аккаунт вручную и попробуйте снова. 🔄"
            )

        except AuthKeyDuplicatedError:
            await telegram_client.disconnect()  # Отключаемся от аккаунта, для освобождения процесса session файла.
            logger.info(f"❌ На данный момент аккаунт {session_name} запущен под другим ip")
            working_with_accounts(f"{account_directory}/{session_name}.session",
                                  f"user_data/accounts/banned/{session_name}.session")
        except AttributeError as error:
            logger.error(f"❌ Ошибка: {error}")
        except ValueError:
            logger.info(f"❌ Ошибка подключения прокси к аккаунту {session_name}.")
        except Exception as error:
            await telegram_client.disconnect()
            logger.exception(f"❌ Ошибка: {error}")

    async def connecting_number_accounts(self, page: ft.Page):
        """
        Подключение номера Telegram аккаунта с проверкой на валидность. Если ранее не было соединения, то запрашивается
        код.

        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            logger.info(f"Подключение номера аккаунта Telegram")

            # Создаем текстовый элемент и добавляем его на страницу
            header_text = ft.Text(f"Подключение аккаунтов Telegram", size=15, color="pink600")

            phone_number = ft.TextField(label="Введите номер телефона:", multiline=False, max_lines=1)

            async def btn_click(e) -> None:
                phone_number_value = phone_number.value
                logger.info(f"Номер телефона: {phone_number_value}")

                # Дальнейшая обработка после записи номера телефона
                proxy_settings = await reading_proxy_data_from_the_database(self.db_handler)  # Proxy IPV6 - НЕ РАБОТАЮТ

                telegram_client = TelegramClient(f"{folder_accounts}/{phone_number_value}",
                                                 api_id=api_id,
                                                 api_hash=api_hash,
                                                 system_version="4.16.30-vxCUSTOM", proxy=proxy_settings)
                await telegram_client.connect()  # Подключаемся к Telegram

                if not await telegram_client.is_user_authorized():
                    logger.info("Пользователь не авторизован")
                    await telegram_client.send_code_request(phone_number_value)  # Отправка кода на телефон
                    await asyncio.sleep(2)

                    passww = ft.TextField(label="Введите код telegram:", multiline=True, max_lines=1)

                    async def btn_click_code(e) -> None:
                        try:
                            logger.info(f"Код telegram: {passww.value}")
                            await telegram_client.sign_in(phone_number_value, passww.value)  # Авторизация с кодом
                            telegram_client.disconnect()
                            page.go(
                                "/connecting_accounts_by_number")  # Перенаправление в настройки, если 2FA не требуется
                            page.update()
                        except SessionPasswordNeededError:  # Если аккаунт защищен паролем, запрашиваем пароль
                            logger.info("❌ Требуется двухфакторная аутентификация. Введите пароль.")
                            pass_2fa = ft.TextField(label="Введите пароль telegram:", multiline=False, max_lines=1)

                            async def btn_click_password(e) -> None:
                                logger.info(f"Пароль telegram: {pass_2fa.value}")
                                try:
                                    await telegram_client.sign_in(password=pass_2fa.value)
                                    logger.info("Успешная авторизация.")
                                    telegram_client.disconnect()
                                    page.go(
                                        "/connecting_accounts_by_number")  # Изменение маршрута в представлении существующих настроек
                                    page.update()
                                except Exception as ex:
                                    logger.exception(f"❌ Ошибка при вводе пароля: {ex}")

                            page.views.append(ft.View(controls=[
                                pass_2fa,
                                await create_buttons(text="✅ Готово", on_click=btn_click_password),
                            ]))
                            page.update()  # Обновляем страницу, чтобы интерфейс отобразился

                        except ApiIdInvalidError:
                            logger.error("[!] Неверные API ID или API Hash.")
                            await telegram_client.disconnect()  # Отключаемся от Telegram
                        except Exception as error:
                            logger.exception(f"❌ Ошибка при авторизации: {error}")
                            await telegram_client.disconnect()  # Отключаемся от Telegram

                    page.views.append(ft.View(controls=[passww,
                                                        await create_buttons(text="✅ Готово", on_click=btn_click_code),
                                                        ]))
                    page.update()  # Обновляем страницу, чтобы отобразился интерфейс для ввода кода

                page.update()

            async def back_button_clicked(e):
                """
                Кнопка возврата в меню настроек
                """
                page.go("/connecting_accounts_by_number")

            input_view = ft.View(
                controls=[header_text, phone_number,
                          await create_buttons(text="✅ Готово", on_click=btn_click),
                          await create_buttons(text="⬅️ Назад", on_click=back_button_clicked),
                          ])  # Создаем вид, который будет содержать поле ввода и кнопку

            page.views.append(input_view)  # Добавляем созданный вид на страницу
            page.update()

        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    @staticmethod
    async def connecting_session_accounts(page: ft.Page):
        """
        Подключение сессии Telegram

        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        logger.info(f"Подключение session аккаунта Telegram.")
        try:
            # Создаем текстовый элемент и добавляем его на страницу
            header_text = ft.Text(f"Подключение аккаунтов Telegram.\n\n Выберите session файл\n",
                                  size=15,
                                  # color="pink600"
                                  )

            # Поле для отображения выбранного файла
            selected_files = ft.Text(value="Session файл не выбран", size=12)

            async def btn_click(e: ft.FilePickerResultEvent) -> None:
                """Обработка выбора файла"""
                if e.files:
                    file_name = e.files[0].name  # Имя файла
                    file_path = e.files[0].path  # Путь к файлу

                    # Проверка расширения файла на ".session"
                    if file_name.endswith(".session"):
                        selected_files.value = f"Выбран session файл: {file_name}"
                        selected_files.update()

                        # Определяем целевой путь для копирования файла
                        target_folder = f"{folder_accounts}"
                        target_path = os.path.join(target_folder, file_name)

                        # Создаем директорию, если она не существует
                        os.makedirs(target_folder, exist_ok=True)

                        # Копируем файл
                        shutil.copy(file_path, target_path)
                        selected_files.value = f"Файл скопирован в: {target_path}"
                    else:
                        selected_files.value = "Выбранный файл не является session файлом"
                else:
                    selected_files.value = "Выбор файла отменен"

                selected_files.update()
                page.update()

            async def back_button_clicked(e):
                """Кнопка возврата в меню настроек"""
                page.go("/connecting_accounts_by_session")

            pick_files_dialog = ft.FilePicker(on_result=btn_click)  # Инициализация выбора файлов

            page.overlay.append(pick_files_dialog)  # Добавляем FilePicker на страницу

            # Добавляем все элементы на страницу
            input_view = ft.View(
                controls=[
                    header_text,
                    selected_files,  # Поле для отображения выбранного файла
                    await create_buttons(text="Выбрать session файл",
                                         on_click=lambda _: pick_files_dialog.pick_files()),  # Кнопка выбора файла
                    await create_buttons(text="⬅️ Назад", on_click=back_button_clicked),  # Кнопка возврата
                ]
            )

            page.views.append(input_view)  # Добавляем созданный вид на страницу
            page.update()

        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")
