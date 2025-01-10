import configparser


async def read_config() -> configparser.ConfigParser:
    """
    Читает данные из конфигурационного файла.

    :return: Объект configparser.ConfigParser, содержащий настройки.
    """
    config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
    config.read("src/setting/config.ini")
    return config


if __name__ == '__main__':
    read_config()
