import flet as ft

from src.core.configs import config, program_name, program_version, date_of_program_change

async def actions_with_the_program_window(page: ft.Page):
    """Изменение на изменение главного окна программы."""
    page.title = f"Версия {program_version}. Дата изменения {date_of_program_change}"
    page.window.width = config.WINDOW_WIDTH
    page.window.height = config.WINDOW_HEIGHT
    page.window.resizable = False  # Запрет изменения размера окна
    page.window.min_width = config.WINDOW_WIDTH  # Минимальная ширина
    page.window.max_width = config.WINDOW_WIDTH  # Максимальная ширина
    page.window.min_height = config.WINDOW_HEIGHT  # Минимальная высота
    page.window.max_height = config.WINDOW_HEIGHT  # Максимальная высота



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
            ft.OutlinedButton(text="📋 Получение списка каналов",
                              on_click=lambda _: self.page.go("/getting_list_channels"),
                              width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS), ),
                              ),
            ft.OutlinedButton(text="💬 Отправка комментариев",
                              on_click=lambda _: self.page.go("/submitting_comments"),
                              width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS), ),
                              ),
            ft.OutlinedButton(text="🖼️ Смена имени, описания, фото",
                              on_click=lambda _: self.page.go("/change_name_description_photo"),
                              width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS), ),
                              ),
            ft.OutlinedButton(text="🔗 Подписка на каналы",
                              on_click=lambda _: self.page.go("/channel_subscription"),
                              width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS), ),
                              ),
            ft.OutlinedButton(text="📂 Формирование списка каналов",
                              on_click=lambda _: self.page.go("/creating_list_of_channels"),
                              width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS), ),
                              ),
            ft.OutlinedButton(text="📖 Документация",
                              on_click=lambda _: self.page.go("/documentation"),
                              width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=config.RADIUS), ),
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
