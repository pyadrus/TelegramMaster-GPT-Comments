import flet as ft
from loguru import logger
from src.core.configs import program_version, date_of_program_change, program_name
from src.core.logging_in import loging
from src.gui.app import action_1_with_log, action_2_with_log, action_3, action_4, action_5

# Настройка логирования
logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")

# Константы размеров окна
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 600

class MainMenu:
    """Класс для отображения главного меню."""

    def __init__(self, page: ft.Page, info_field: ft.TextField):
        self.page = page
        self.info_field = info_field
        self.button_width = 700
        self.button_height = 50

    def create_title(self, text: str, font_size: int = 13) -> ft.Text:
        """Создает заголовок с градиентом."""
        return ft.Text(
            spans=[
                ft.TextSpan(
                    text,
                    ft.TextStyle(
                        size=font_size,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [ft.colors.RED, ft.colors.RED]
                            )
                        ),
                    ),
                ),
            ],
        )

    def create_buttons(self) -> list:
        """Создает список кнопок меню."""
        return [
            ft.ElevatedButton(
                text="Получение списка каналов",
                on_click=lambda _: action_1_with_log(self.page, self.info_field),
                width=self.button_width,
                height=self.button_height,
            ),
            ft.ElevatedButton(
                text="Отправка комментариев",
                on_click=lambda _: action_2_with_log(self.page, self.info_field),
                width=self.button_width,
                height=self.button_height,
            ),
            ft.ElevatedButton(
                text="Смена имени, описания, фото",
                on_click=lambda _: action_3(self.page, self.info_field),
                width=self.button_width,
                height=self.button_height,
            ),
            ft.ElevatedButton(
                text="Подписка на каналы",
                on_click=lambda _: action_4(self.page, self.info_field),
                width=self.button_width,
                height=self.button_height,
            ),
            ft.ElevatedButton(
                text="Формирование списка каналов",
                on_click=lambda _: action_5(self.page, self.info_field),
                width=self.button_width,
                height=self.button_height,
            ),
        ]

    def build(self) -> ft.Column:
        """Создает колонку с заголовками и кнопками."""
        title = self.create_title(program_name, font_size=15)
        version = self.create_title(program_version)
        buttons = self.create_buttons()
        return ft.Column(
            [title, version, *buttons],
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
        )


class Application:
    """Класс для управления приложением."""

    def __init__(self):
        self.page = None

    async def setup(self, page: ft.Page):
        """Настраивает страницу."""
        self.page = page
        await loging()

        page.title = f"Версия {program_version}. Дата изменения {date_of_program_change}"
        page.window.width = WINDOW_WIDTH
        page.window.height = WINDOW_HEIGHT
        page.window.resizable = False

        # Поле для вывода информации
        info_field = ft.TextField(
            multiline=True,
            expand=True,
            width=300,
            label="Информация",
            value="Тут будет выводиться информация...",
        )

        # Создаем главное меню
        menu = MainMenu(page, info_field).build()

        # Создаем макет
        layout = ft.Row(
            [
                ft.Container(menu, width=250, padding=20),
                ft.Container(info_field, expand=True, padding=20),
            ],
            alignment=ft.MainAxisAlignment.START,
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
