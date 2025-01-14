from loguru import logger
import flet as ft

# Настройка логирования
logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")

# Константы
program_version = "0.0.7"
date_of_program_change = "12.01.2025"
program_name = "TelegramMaster_Commentator"
PADDING = 10
SPACING = 5
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 40
BUTTON_WIDTH_RadyAndBackButtons = 540
BUTTON_HEIGHT_RadyAndBackButtons = 35
PROGRAM_MENU_WIDTH = BUTTON_WIDTH + PADDING
RADIUS = 5
PRIMARY_COLOR = ft.colors.CYAN_600
SECONDARY_COLOR = ft.colors.BLACK
TITLE_FONT_SIZE = 13
TITLE_FONT_WEIGHT = ft.FontWeight.BOLD
LINE_WIDTH = 1
LINE_COLOR = ft.colors.GREY

async def actions_with_the_program_window(page: ft.Page):
    """Изменение на изменение главного окна программы."""
    page.title = f"Версия {program_version}. Дата изменения {date_of_program_change}"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.window.min_width = WINDOW_WIDTH
    page.window.max_width = WINDOW_WIDTH
    page.window.min_height = WINDOW_HEIGHT
    page.window.max_height = WINDOW_HEIGHT

class MainMenu:
    """Класс для отображения главного меню."""

    def __init__(self, page: ft.Page, info_list: ft.ListView):
        self.page = page
        self.info_list = info_list

    def create_title(self, text: str, font_size: int = TITLE_FONT_SIZE) -> ft.Text:
        """Создает заголовок с градиентом."""
        return ft.Text(
            spans=[
                ft.TextSpan(
                    text,
                    ft.TextStyle(
                        size=font_size,
                        weight=TITLE_FONT_WEIGHT,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [PRIMARY_COLOR, PRIMARY_COLOR]
                            )), ), ), ], )

    def create_button(self, text: str, route: str) -> ft.OutlinedButton:
        """Создает кнопку меню."""
        return ft.OutlinedButton(
            text=text,
            on_click=lambda _: self.page.go(route),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS)),
        )

    def build(self) -> ft.Column:
        """Создает колонку с заголовками и кнопками."""
        title = self.create_title(text=program_name, font_size=19)
        version = self.create_title(text=f"Версия программы: {program_version}", font_size=13)
        date_program_change = self.create_title(text=f"Дата изменения: {date_of_program_change}", font_size=13)
        buttons = [
            self.create_button("📋 Получение списка каналов", "/getting_list_channels"),
            self.create_button("💬 Отправка комментариев", "/submitting_comments"),
            self.create_button("🖼️ Смена имени, описания, фото", "/change_name_description_photo"),
            self.create_button("🔗 Подписка на каналы", "/channel_subscription"),
            self.create_button("📂 Формирование списка каналов", "/creating_list_of_channels"),
            self.create_button("📖 Документация", "/documentation"),
        ]
        return ft.Column(
            [title, version, date_program_change, *buttons],
            alignment=ft.MainAxisAlignment.START,
            spacing=SPACING,
        )

class Application:
    """Класс для управления приложением."""

    def __init__(self):
        self.page = None
        self.info_list = None
        self.menu = None

    async def setup(self):
        """Настраивает страницу."""
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.on_route_change = self.route_change

        await actions_with_the_program_window(self.page)

        self._add_startup_message()
        await self.route_change(None)

    def _add_startup_message(self):
        """Добавляет стартовое сообщение в ListView."""
        self.info_list.controls.append(
            ft.Text(
                "TelegramMaster Commentator 🚀\n\nTelegramMaster Commentator - это программа для автоматической "
                "расставления комментариев в каналах Telegram, а также для работы с аккаунтами. 💬\n\n"
                "📂 Проект доступен на GitHub: https://github.com/pyadrus/TelegramMaster_Commentator \n"
                "📲 Контакт с разработчиком в Telegram: https://t.me/PyAdminRU\n"
                f"📡 Информация на канале: https://t.me/master_tg_d"
            )
        )

    async def route_change(self, route):
        """Обработчик изменения маршрута."""
        self.page.views.clear()

        layout = ft.Row(
            [
                ft.Container(self.menu, width=PROGRAM_MENU_WIDTH, padding=PADDING),
                ft.Container(width=LINE_WIDTH, bgcolor=LINE_COLOR),
                ft.Container(self.info_list, expand=True, padding=PADDING),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            expand=True,
        )

        self.page.views.append(ft.View("/", [layout]))

        route_handlers = {
            "/getting_list_channels": self._handle_getting_list_channels,
            "/submitting_comments": self._handle_submitting_comments,
            "/change_name_description_photo": self._handle_change_name_description_photo,
            "/channel_subscription": self._handle_channel_subscription,
            "/creating_list_of_channels": self._handle_creating_list_of_channels,
            "/documentation": self._handle_documentation,
            "/errors": self._handle_errors,
        }

        handler = route_handlers.get(self.page.route)
        if handler:
            await handler()

        self.page.update()

    async def _add_back_button(self):
        """Добавляет кнопку 'Назад' на страницу."""
        back_button = ft.ElevatedButton("Назад", on_click=lambda _: self.page.go("/"))
        self.info_list.controls.append(back_button)
        self.page.update()

    async def _handle_getting_list_channels(self):
        logger.info("Получение списка каналов")
        await self._add_back_button()

    async def _handle_submitting_comments(self):
        logger.info("Отправка комментариев")
        await self._add_back_button()

    async def _handle_change_name_description_photo(self):
        logger.info("Смена имени, описания, фото")
        await self._add_back_button()

    async def _handle_channel_subscription(self):
        logger.info("Подписка на каналы")
        await self._add_back_button()

    async def _handle_creating_list_of_channels(self):
        logger.info("Формирование списка каналов")
        await self._add_back_button()

    async def _handle_documentation(self):
        logger.info("Документация")
        await self._add_back_button()

    async def _handle_errors(self):
        logger.info("Ошибка")
        await self._add_back_button()

    async def main(self, page: ft.Page):
        """Точка входа в приложение."""
        self.page = page
        self.info_list = ft.ListView(expand=True, spacing=10, padding=PADDING, auto_scroll=True)
        self.menu = MainMenu(page, self.info_list).build()
        await self.setup()

if __name__ == "__main__":
    ft.app(target=Application().main)