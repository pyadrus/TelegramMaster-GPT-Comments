# -*- coding: utf-8 -*-
import configparser


class ConfigReader:
    """
    Класс для чтения и обработки конфигурационных файлов.

    Этот класс предоставляет методы для извлечения настроек из двух конфигурационных файлов:
    - `config.ini`: содержит настройки, связанные с Telegram.
    - `config_gui.ini`: содержит настройки, связанные с графическим интерфейсом программы.

    Attributes:
        config_gui (configparser.ConfigParser): Парсер для файла `config_gui.ini`.
        config (configparser.ConfigParser): Парсер для файла `config.ini`.
    """

    def __init__(self):
        """
        Инициализирует объект ConfigReader и загружает конфигурационные файлы.
        """
        self.config_gui = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
        self.config_gui.read('data/config/config_gui.ini')
        self.config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
        self.config.read('data/config/config.ini')
        self.config_path = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
        self.config_path.read('data/config/config_path.ini')

    def get_time_config_settings(self):
        """
        Извлекает введенное время пользователем из конфигурационного файла.
        """
        return self.config.get("time_config", "time_config", fallback=None)

    def get_path_db(self):
        """
        Извлекает путь к папке с базой данных из конфигурационного файла.
        """
        return self.config_path.get("db_path", "db_path", fallback=None)

    def get_path_account(self):
        """
        Извлекает путь к папке с файлами из конфигурационного файла.
        """
        return (
            self.config_path.get("folder_accounts", "folder_accounts", fallback=None)
        )

    def get_path_log(self):
        """
        Извлекает путь к папке с файлами из конфигурационного файла.
        """
        return (
            self.config_path.get("log_file", "app_log", fallback=None),
            self.config_path.get("log_file", "errors_log", fallback=None)
        )

    def get_telegram_credentials(self):
        """
        Извлекает учетные данные Telegram из конфигурационного файла.

        :return: Кортеж, содержащий `api_id` и `api_hash`. Если значения отсутствуют, возвращает (None, None).
        """
        return (
            self.config.get("telegram_settings", "id", fallback=None),
            self.config.get("telegram_settings", "hash", fallback=None)
        )

    def get_program_version(self) -> str | None:
        """
        Извлекает версию программы из конфигурационного файла.

        :return: Версия программы. Если значение отсутствует, возвращает None.
        """
        return self.config_gui.get("program_version", "program_version", fallback=None)

    def get_program_last_modified_date(self) -> str | None:
        """
        Извлекает дату последнего изменения программы из конфигурационного файла.

        :return: Дата последнего изменения программы. Если значение отсутствует, возвращает None.
        """
        return self.config_gui.get("date_of_program_change", "date_of_program_change", fallback=None)

    def get_program_name(self) -> str | None:
        """
        Извлекает название программы из конфигурационного файла.

        :return: Название программы. Если значение отсутствует, возвращает None.
        """
        return self.config_gui.get("program_name", "program_name", fallback=None)

    def get_program_window_width(self) -> int | None:
        """
        Извлекает ширину окна программы из конфигурационного файла.
        :return: Ширина окна программы. Если значение отсутствует, возвращает None.
        """
        return self.config_gui.get("WINDOW_WIDTH", "WINDOW_WIDTH", fallback=None)

WINDOW_WIDTH = ConfigReader().get_program_window_width()  # Извлечение ширины окна из конфигурационного файла

# Инициализация глобальных переменных с настройками
program_version = ConfigReader().get_program_version()
program_last_modified_date = ConfigReader().get_program_last_modified_date()
program_name = ConfigReader().get_program_name()
telegram_credentials = ConfigReader().get_telegram_credentials()

# Разделение учетных данных Telegram на отдельные переменные
api_id, api_hash = ConfigReader().get_telegram_credentials()

# Путь к файлам
app_log, errors_log = ConfigReader().get_path_log()
# Путь к папке с аккаунтами
folder_accounts = ConfigReader().get_path_account()
# Путь к базе данных
db_path = ConfigReader().get_path_db()
# Извлечение времени задержки в секундах
time_config = ConfigReader().get_time_config_settings()
