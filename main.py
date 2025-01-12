import flet as ft
from loguru import logger
from src.core.configs import program_version, date_of_program_change, program_name
from src.core.logging_in import loging
from src.gui.app import action_1_with_log, action_2_with_log, action_3, action_4, action_5

# Настройка логирования
logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")


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


class MainMenu:
    """Класс для отображения главного меню."""

    def __init__(self, page: ft.Page, info_list: ft.ListView):
        self.page = page  # страница
        self.info_list = info_list  # ListView для вывода текста

    def create_title(self, text: str, font_size: int = config.TITLE_FONT_SIZE) -> ft.Text:
        """Создает заголовок с градиентом."""
        return ft.Text(
            spans=[
                ft.TextSpan(
                    text,
                    ft.TextStyle(
                        size=font_size,
                        weight=config.TITLE_FONT_WEIGHT,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [config.PRIMARY_COLOR, config.PRIMARY_COLOR]
                            )), ), ), ], )

    def create_buttons(self) -> list:
        """Создает список кнопок меню."""
        return [
            ft.OutlinedButton(
                text="📋 Получение списка каналов",
                on_click=lambda _: action_1_with_log(self.page, self.info_list),
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=config.RADIUS),
                ),
            ),
            ft.OutlinedButton(
                text="💬 Отправка комментариев",
                on_click=lambda _: action_2_with_log(self.page, self.info_list),
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=config.RADIUS),
                ),
            ),
            ft.OutlinedButton(
                text="🖼️ Смена имени, описания, фото",
                on_click=lambda _: action_3(self.page, self.info_list),
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=config.RADIUS),
                ),
            ),
            ft.OutlinedButton(
                text="🔗 Подписка на каналы",
                on_click=lambda _: action_4(self.page, self.info_list),
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=config.RADIUS),
                ),
            ),
            ft.OutlinedButton(
                text="📂 Формирование списка каналов",
                on_click=lambda _: action_5(self.page, self.info_list),
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=config.RADIUS),
                ),
            ),
            ft.OutlinedButton(
                text="📖 Документация",
                on_click=lambda _: action_5(self.page, self.info_list),
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=config.RADIUS),
                ),
            ),
        ]

    def build(self) -> ft.Column:
        """Создает колонку с заголовками и кнопками."""
        title = self.create_title(text=program_name, font_size=19)
        version = self.create_title(text=f"Версия программы: {program_version}", font_size=13)
        date_program_change = self.create_title(text=f"Дата изменения: {date_of_program_change}", font_size=13)
        buttons = self.create_buttons()
        return ft.Column(
            [title, version, date_program_change, *buttons],
            alignment=ft.MainAxisAlignment.START,
            spacing=config.SPACING,
        )


class Application:
    """Класс для управления приложением."""

    def __init__(self):
        self.page = None

    async def setup(self, page: ft.Page):
        """Настраивает страницу."""
        self.page = page

        # Установка светлой темы
        self.page.theme_mode = ft.ThemeMode.LIGHT

        await loging()

        page.title = f"Версия {program_version}. Дата изменения {date_of_program_change}"
        page.window.width = config.WINDOW_WIDTH
        page.window.height = config.WINDOW_HEIGHT
        page.window.resizable = False  # Запрет изменения размера окна
        page.window.min_width = config.WINDOW_WIDTH  # Минимальная ширина
        page.window.max_width = config.WINDOW_WIDTH  # Максимальная ширина
        page.window.min_height = config.WINDOW_HEIGHT  # Минимальная высота
        page.window.max_height = config.WINDOW_HEIGHT  # Максимальная высота

        # Поле для вывода информации
        info_list = ft.ListView(expand=True, spacing=10, padding=config.PADDING, auto_scroll=True)

        # Добавляем стартовое сообщение в ListView
        info_list.controls.append(ft.Text(
            "TelegramMaster Commentator 🚀\n\nTelegramMaster Commentator - это программа для автоматической расставления комментариев в каналах Telegram, а также для работы с аккаунтами. 💬\n\n"
            "📂 Проект доступен на GitHub: https://github.com/pyadrus/TelegramMaster_Commentator \n"
            "📲 Контакт с разработчиком в Telegram: https://t.me/PyAdminRU\n"
            f"📡 Информация на канале: https://t.me/master_tg_d", ))

        # Создаем главное меню
        menu = MainMenu(page, info_list).build()

        layout = ft.Row(
            [
                ft.Container(menu, width=config.PROGRAM_MENU_WIDTH, padding=config.PADDING),
                ft.Container(width=config.LINE_WIDTH, bgcolor=config.LINE_COLOR),  # Вертикальная линия
                ft.Container(info_list, expand=True, padding=config.PADDING),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,  # Убираем промежуток между элементами
            expand=True,
        )

        # Добавляем макет на страницу
        page.add(layout)
        page.update()

    async def main(self, page: ft.Page):
        """Точка входа в приложение."""
        await self.setup(page)


if __name__ == "__main__":
    app = Application()
    ft.app(target=app.main)
