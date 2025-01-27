import flet as ft
from loguru import logger

from src.config_handler import program_version, program_last_modified_date, program_name
from src.core.handlers import (handle_getting_list_channels, handle_documentation,
                               handle_creating_list_of_channels, handle_channel_subscription,
                               handle_submitting_comments, handle_change_name_description_photo,
                               handle_connect_accounts, handle_settings)
from src.core.views import PRIMARY_COLOR, TITLE_FONT_WEIGHT
from src.logging_in import loging
from src.settings import SettingPage

# Настройка логирования
logger.add("data/logs/app.log", rotation="500 KB", compression="zip", level="INFO")
logger.add("data/logs/errors.log", rotation="500 KB", compression="zip", level="ERROR")


class Application:
    """Класс для управления приложением."""

    def __init__(self):
        self.page = None
        self.info_list = None
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 600
        self.SPACING = 5
        self.RADIUS = 5
        self.LINE_COLOR = ft.colors.GREY
        self.BUTTON_HEIGHT = 40
        self.LINE_WIDTH = 1
        self.PADDING = 10
        self.BUTTON_WIDTH = 300
        self.PROGRAM_MENU_WIDTH = self.BUTTON_WIDTH + self.PADDING

    async def actions_with_the_program_window(self, page: ft.Page):
        """Изменение на изменение главного окна программы."""
        page.title = f"Версия {program_version}. Дата изменения {program_last_modified_date}"
        page.window.width = self.WINDOW_WIDTH
        page.window.height = self.WINDOW_HEIGHT
        page.window.resizable = False
        page.window.min_width = self.WINDOW_WIDTH
        page.window.max_width = self.WINDOW_WIDTH
        page.window.min_height = self.WINDOW_HEIGHT
        page.window.max_height = self.WINDOW_HEIGHT

    def create_title(self, text: str, font_size) -> ft.Text:
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
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=self.RADIUS)),
        )

    def build_menu(self) -> ft.Column:
        """Создает колонку с заголовками и кнопками."""
        title = self.create_title(text=program_name, font_size=19)
        version = self.create_title(text=f"Версия программы: {program_version}", font_size=13)
        date_program_change = self.create_title(text=f"Дата изменения: {program_last_modified_date}", font_size=13)
        buttons = [
            self.create_button("📋 Получение списка каналов", "/getting_list_channels"),
            self.create_button("💬 Отправка комментариев", "/submitting_comments"),
            self.create_button("🖼️ Смена имени, описания, фото", "/change_name_description_photo"),
            self.create_button("🔗 Подписка на каналы", "/channel_subscription"),
            self.create_button("📂 Формирование списка каналов", "/creating_list_of_channels"),
            self.create_button("📖 Документация", "/documentation"),
            self.create_button("🔗 Подключение аккаунтов", "/connect_accounts"),
            self.create_button("⚙️ Настройки программы", "/settings"),
        ]
        return ft.Column(
            [title, version, date_program_change, *buttons],
            alignment=ft.MainAxisAlignment.START,
            spacing=self.SPACING,
        )

    async def setup(self):
        """Настраивает страницу."""
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.on_route_change = self.route_change
        await self.actions_with_the_program_window(self.page)
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
                ft.Container(self.build_menu(), width=self.PROGRAM_MENU_WIDTH, padding=self.PADDING),
                ft.Container(width=self.LINE_WIDTH, bgcolor=self.LINE_COLOR),
                ft.Container(self.info_list, expand=True, padding=self.PADDING),
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
            "/connect_accounts": self._handle_connect_accounts,
            "/settings": self._handle_settings,
            "/settings_proxy": self._handle_settings_proxy,
            "/record_id_hash": self._handle_record_id_hash,
            "/recording_message": self._recording_message,
            "/record_time": self._handle_record_time,
        }
        handler = route_handlers.get(self.page.route)
        if handler:
            await handler()
        self.page.update()

    async def _handle_record_time(self):
        """Страница Запись времени"""
        limit_type = "time_config"
        label = "Введите время в секундах, в цифрах"  # Подпись в поле ввода
        await SettingPage().record_setting(self.page, limit_type, label)

    async def _recording_message(self):
        """Страница Запись сообщения"""
        unique_filename = "data/message/message"
        label = "Введите сообщение, которое будет отправляться в канал"
        await SettingPage().recording_text_for_sending_messages(self.page, label, unique_filename)

    async def _handle_record_id_hash(self):
        """Страница Запись id и hash"""
        await SettingPage().writing_api_id_api_hash(self.page)

    async def _handle_settings_proxy(self):
        """Страница ⚙️ Настройки прокси"""
        await SettingPage().creating_the_main_window_for_proxy_data_entry(self.page)

    async def _handle_connect_accounts(self):
        """Страница 🔗 Подключение аккаунтов"""
        await handle_connect_accounts(self.page)

    async def _handle_settings(self):
        """Страница ⚙️ Настройки программы"""
        await handle_settings(self.page)

    async def _handle_getting_list_channels(self):
        """Страница 📋 Получение списка каналов"""
        await handle_getting_list_channels(self.page)

    async def _handle_submitting_comments(self):
        """Страница 💬 Отправка комментариев"""
        await handle_submitting_comments(self.page)

    async def _handle_change_name_description_photo(self):
        """Страница 🖼️ Смена имени, описания, фото"""
        await handle_change_name_description_photo(self.page)

    async def _handle_channel_subscription(self):
        """Страница 🔗 Подписка на каналы"""
        await handle_channel_subscription(self.page)

    async def _handle_creating_list_of_channels(self):
        """Страница 📂 Формирование списка каналов"""
        await handle_creating_list_of_channels(self.page)

    async def _handle_documentation(self):
        """Страница 📖 Документация"""
        await handle_documentation(self.page)

    async def main(self, page: ft.Page):
        """Точка входа в приложение."""
        self.page = page
        self.info_list = ft.ListView(expand=True, spacing=10, padding=self.PADDING, auto_scroll=True)

        await self.setup()
        await loging()


if __name__ == "__main__":
    ft.app(target=Application().main)
