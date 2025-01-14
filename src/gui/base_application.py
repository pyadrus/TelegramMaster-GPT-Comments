import flet as ft

from src.core.configs import config
from src.core.logging_in import loging
from src.gui.main_menu import MainMenu, actions_with_the_program_window


class BaseApplication:
    """Базовый класс для управления приложением."""

    def __init__(self, page: ft.Page, info_list: ft.ListView):
        self.page = page
        self.info_list = info_list

    async def setup(self, page: ft.Page):
        """Настраивает страницу."""
        self.page = page

        # Установка светлой темы
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Привязка обработчика маршрутов
        self.page.on_route_change = self.route_change

        await loging()

        await actions_with_the_program_window(page)

        # Поле для вывода информации
        self.info_list = ft.ListView(expand=True, spacing=10, padding=config.PADDING, auto_scroll=True)

        # Создаем главное меню
        self.menu = MainMenu(page, self.info_list).build()

        # Инициализация начального маршрута
        await self.route_change(None)

    async def route_change(self, route):
        """Обработчик изменения маршрута."""
        self.page.views.clear()

        # Основной макет (боковое меню и информационная панель)
        layout = self.create_layout()
        self.page.views.append(ft.View("/", [layout]))

        self.page.update()

    def create_layout(self) -> ft.Row:
        """Создает основной макет страницы."""
        main_content = ft.Column(
            [
                ft.Container(self.info_list, expand=True, padding=config.PADDING),
                ft.Container(
                    self.create_bottom_buttons(),
                    alignment=ft.alignment.bottom_center,
                    padding=ft.padding.only(bottom=20),  # Отступ снизу
                ),
            ],
            expand=True,
        )

        return ft.Row(
            [
                ft.Container(self.menu, width=config.PROGRAM_MENU_WIDTH, padding=config.PADDING),
                ft.Container(width=config.LINE_WIDTH, bgcolor=config.LINE_COLOR),  # Вертикальная линия
                main_content,  # Основной контент и кнопки внизу
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,  # Убираем промежуток между элементами
            expand=True,
        )

    def create_bottom_buttons(self) -> ft.Column:
        """Создает кнопки внизу страницы."""
        buttons = self.create_buttons()
        return ft.Column(
            [*buttons],
            alignment=ft.MainAxisAlignment.START,
            spacing=config.SPACING,
        )

    def create_buttons(self) -> list:
        """Создает список кнопок. Должен быть переопределен в дочерних классах."""
        raise NotImplementedError("Метод create_buttons должен быть переопределен в дочерних классах.")
