import flet as ft

from src.core.configs import config
from src.core.logging_in import loging
from src.core.main_menu import MainMenu, actions_with_the_program_window


class RadyAndBackButtons:
    """Кнопки назад и начать"""

    def __init__(self, page: ft.Page, info_list: ft.ListView):
        self.page = page  # страница
        self.info_list = info_list  # ListView для вывода текста

    def create_buttons(self) -> list:
        """Создает список кнопок."""
        return [
            ft.OutlinedButton(
                text="Получить список каналов",
                on_click=lambda _: self.page.go("/getting_list_channels"),
                width=config.BUTTON_WIDTH_RadyAndBackButtons,
                height=config.BUTTON_HEIGHT_RadyAndBackButtons,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS)),
            ),
        ]

    def build(self) -> ft.Column:
        """Создает колонку с кнопками."""
        buttons = self.create_buttons()
        return ft.Column(
            [*buttons],
            alignment=ft.MainAxisAlignment.START,
            spacing=config.SPACING,
        )


class ApplicationGettingListChannels:
    """Класс для управления приложением."""

    def __init__(self):
        self.page = None

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

        # Добавляем стартовое сообщение в ListView
        self.info_list.controls.append(
            ft.Text(
                "Получение списка каналов\n\n"
            )
        )

        # Создаем главное меню
        self.menu = MainMenu(page, self.info_list).build()
        self.rady_and_back_buttons = RadyAndBackButtons(page, self.info_list).build()

        # Инициализация начального маршрута
        await self.route_change(None)

    async def route_change(self, route):
        """Обработчик изменения маршрута."""
        self.page.views.clear()

        # Основной макет (боковое меню и информационная панель)
        main_content = ft.Column(
            [
                ft.Container(self.info_list, expand=True, padding=config.PADDING),
                ft.Container(
                    self.rady_and_back_buttons,
                    alignment=ft.alignment.bottom_center,
                    padding=ft.padding.only(bottom=20),  # Отступ снизу
                ),
            ],
            expand=True,
        )

        # Основной макет страницы
        layout = ft.Row(
            [
                ft.Container(self.menu, width=config.PROGRAM_MENU_WIDTH, padding=config.PADDING),
                ft.Container(width=config.LINE_WIDTH, bgcolor=config.LINE_COLOR),  # Вертикальная линия
                main_content,  # Основной контент и кнопки внизу
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,  # Убираем промежуток между элементами
            expand=True,
        )

        # Добавляем макет на страницу
        self.page.views.append(ft.View("/", [layout]))

        self.page.update()

    async def ApplicationGettingListChannels_main(self, page: ft.Page):
        """Точка входа в приложение."""
        await self.setup(page)
