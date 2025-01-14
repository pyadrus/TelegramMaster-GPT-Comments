import flet as ft

program_version = "0.0.7"
date_of_program_change = "12.01.2025"
program_name = "TelegramMaster_Commentator"


class AppConfig:
    """Класс для хранения конфигурации приложения."""

    # Отступы и padding
    PADDING = 10  # Отступ от левого бокового меню (кнопок) и разделительной линии
    SPACING = 5  # Отступы между кнопками

    # Размеры окна
    WINDOW_WIDTH = 900  # ширина окна
    WINDOW_HEIGHT = 600  # высота окна

    # Размеры кнопок
    BUTTON_WIDTH = 300  # ширина кнопки
    BUTTON_HEIGHT = 40  # высота кнопки

    # Размеры кнопок Получить список каналов и На главную
    BUTTON_WIDTH_RadyAndBackButtons = 540
    BUTTON_HEIGHT_RadyAndBackButtons = 35

    # Ширина бокового меню
    PROGRAM_MENU_WIDTH = BUTTON_WIDTH + PADDING

    # Закругление кнопок
    RADIUS = 5  # Если значение равно 0, то кнопки не закруглены

    # Цвета
    PRIMARY_COLOR = ft.colors.CYAN_600
    SECONDARY_COLOR = ft.colors.BLACK

    # Стили текста
    TITLE_FONT_SIZE = 13
    TITLE_FONT_WEIGHT = ft.FontWeight.BOLD

    # Вертикальная линия
    LINE_WIDTH = 1  # ширина линии
    LINE_COLOR = ft.colors.GREY  # цвет линии


# Конфигурация приложения
config = AppConfig()
