import configparser


class ConfigReader:
    """Чтение конфигурационного файла."""

    def __init__(self):
        self.config_gui = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
        self.config_gui.read('src/setting/config_gui.ini')
        self.config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
        self.config.read('src/setting/config.ini')

    def read_config_telegram_token(self):
        """
        Читает данные из конфигурационного файла.
        """
        return (
            self.config.get("telegram_settings", "id", fallback=None),
            self.config.get("telegram_settings", "hash", fallback=None)
        )

    def read_config_gui_program_version(self) -> str | None:
        """
        Читает данные из конфигурационного файла (gui).
        """
        return self.config_gui.get("program_version", "program_version", fallback=None)

    def read_config_gui_date_of_program_change(self) -> str | None:
        """
        Читает данные из конфигурационного файла (gui).
        """
        return self.config_gui.get("date_of_program_change", "date_of_program_change", fallback=None)

    def read_config_gui_program_name(self) -> str | None:
        """
        Читает данные из конфигурационного файла (gui).
        """
        return self.config_gui.get("program_name", "program_name", fallback=None)


program_version = ConfigReader().read_config_gui_program_version()
date_of_program_change = ConfigReader().read_config_gui_date_of_program_change()
program_name = ConfigReader().read_config_gui_program_name()
telegram_token = ConfigReader().read_config_telegram_token()

api_id, api_hash = ConfigReader().read_config_telegram_token()
