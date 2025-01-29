# -*- coding: utf-8 -*-
import asyncio
import os
import os.path
import random
import shutil

import flet as ft  # Импортируем библиотеку flet
from loguru import logger
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ApiIdInvalidError

from src.config_handler import api_id, api_hash, folder_accounts
from src.core.buttons import create_buttons
from src.db_handler import DatabaseHandler

# Наименование кнопок
back_button: str = "⬅️ Назад"
done_button: str = "✅ Готово"

height_button = 35
line_width_button = 850


async def reading_proxy_data_from_the_database():
    """
    Считываем данные для proxy c базы данных "software_database.db", таблица "proxy" где:
    proxy_type - тип proxy (например: SOCKS5), addr - адрес (например: 194.67.248.9), port - порт (например: 9795)
    username - логин (например: username), password - пароль (например: password)

    """
    try:
        proxy_random_list = random.choice(await DatabaseHandler().open_and_read_data("proxy"))
        logger.info(f"{proxy_random_list}")
        proxy = {'proxy_type': (proxy_random_list[0]), 'addr': proxy_random_list[1], 'port': int(proxy_random_list[2]),
                 'username': proxy_random_list[3], 'password': proxy_random_list[4], 'rdns': proxy_random_list[5]}
        return proxy
    except IndexError:
        proxy = None
        return proxy
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


class TGConnect:

    def __init__(self):
        self.db_handler = DatabaseHandler()

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
                proxy_settings = await reading_proxy_data_from_the_database()  # Proxy IPV6 - НЕ РАБОТАЮТ

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
