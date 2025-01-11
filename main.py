import flet as ft
from loguru import logger
from src.core.configs import program_version, date_of_program_change, program_name
from src.core.logging_in import loging
from src.gui.app import action_1_with_log, action_2_with_log, action_3, action_4, action_5

# Настройка логирования
logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")

# Константы размеров окна
WINDOW_WIDTH = 850 # ширина окна
WINDOW_HEIGHT = 600 # высота окна


class MainMenu:
    """Класс для отображения главного меню."""

    def __init__(self, page: ft.Page, info_list: ft.ListView):
        self.page = page  # страница
        self.info_list = info_list  # ListView для вывода текста
        self.button_width = 700  # ширина кнопок
        self.button_height = 60  # высота кнопок

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
            ft.OutlinedButton(
                text="Получение списка каналов",
                on_click=lambda _: action_1_with_log(self.page, self.info_list),
                width=self.button_width,
                height=self.button_height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.OutlinedButton(
                text="Отправка комментариев",
                on_click=lambda _: action_2_with_log(self.page, self.info_list),
                width=self.button_width,
                height=self.button_height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.OutlinedButton(
                text="Смена имени, описания, фото",
                on_click=lambda _: action_3(self.page, self.info_list),
                width=self.button_width,
                height=self.button_height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.OutlinedButton(
                text="Подписка на каналы",
                on_click=lambda _: action_4(self.page, self.info_list),
                width=self.button_width,
                height=self.button_height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.OutlinedButton(
                text="Формирование списка каналов",
                on_click=lambda _: action_5(self.page, self.info_list),
                width=self.button_width,
                height=self.button_height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
        ]

    def build(self) -> ft.Column:
        """Создает колонку с заголовками и кнопками."""
        title = self.create_title(program_name, font_size=13)
        version = self.create_title(program_version, font_size=13)
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
        info_list = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

        # Добавляем стартовое сообщение в ListView
        info_list.controls.append(ft.Text("TelegramMaster Commentator 🚀\n\nTelegramMaster Commentator 🚀 - это программа для автоматической расставления комментариев в каналах Telegram, а также для работы с аккаунтами.💬\n\n"
        "Проект доступен на GitHub: https://github.com/pyadrus/TelegramMaster_Commentator 📂\n\n"
        "Контакт с разработчиком в Telegram: https://t.me/PyAdminRU 📲\n\n"
        "Информация на канале: https://t.me/master_tg_d 📡",))

        # Создаем главное меню
        menu = MainMenu(page, info_list).build()

        layout = ft.Row(
            [
                ft.Container(menu, width=300, padding=20),
                ft.Container(info_list, expand=True, padding=20),
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
