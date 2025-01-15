from loguru import logger
import flet as ft

from src.config.config_handler import read_config
from src.core.telegram_client import connect_telegram_account
from src.database.db_handler import creating_a_channel_list

# Настройка логирования
logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")


class Application:
    """Класс для управления приложением."""

    def __init__(self):
        self.page = None
        self.info_list = None
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 600
        self.program_version = "0.0.7"
        self.date_of_program_change = "12.01.2025"
        self.program_name = "TelegramMaster_Commentator"
        self.SPACING = 5
        self.RADIUS = 5
        self.PRIMARY_COLOR = ft.colors.CYAN_600
        self.LINE_COLOR = ft.colors.GREY
        self.BUTTON_HEIGHT = 40
        self.LINE_WIDTH = 1
        self.TITLE_FONT_WEIGHT = ft.FontWeight.BOLD
        self.PADDING = 10
        self.BUTTON_WIDTH = 300
        self.PROGRAM_MENU_WIDTH = self.BUTTON_WIDTH + self.PADDING

    async def actions_with_the_program_window(self, page: ft.Page):
        """Изменение на изменение главного окна программы."""
        page.title = f"Версия {self.program_version}. Дата изменения {self.date_of_program_change}"
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
                        weight=self.TITLE_FONT_WEIGHT,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [self.PRIMARY_COLOR, self.PRIMARY_COLOR]
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
        title = self.create_title(text=self.program_name, font_size=19)
        version = self.create_title(text=f"Версия программы: {self.program_version}", font_size=13)
        date_program_change = self.create_title(text=f"Дата изменения: {self.date_of_program_change}", font_size=13)
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
        }
        handler = route_handlers.get(self.page.route)
        if handler:
            await handler()
        self.page.update()

    async def _handle_getting_list_channels(self):
        """Страница Получение списка каналов"""
        await self.getting_list_channels(self.page)

    async def _handle_submitting_comments(self):
        """Страница Отправка комментариев"""
        await self.submitting_comments(self.page)

    async def _handle_change_name_description_photo(self):
        """Страница Смена имени, описания, фото"""
        await self.change_name_description_photo(self.page)

    async def _handle_channel_subscription(self):
        """Страница Подписка на каналы"""
        await self.channel_subscription(self.page)

    async def _handle_creating_list_of_channels(self):
        """Страница Формирование списка каналов"""
        await self.creating_list_of_channels(self.page)

    async def _handle_documentation(self):
        """Страница документации"""
        await self.documentation(self.page)

    async def submitting_comments(self, page: ft.Page):
        """Создает страницу Отправка комментариев"""
        logger.info("Пользователь перешел на страницу Отправка комментариев")
        page.views.clear()  # Очищаем страницу и добавляем новый View
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения информации
        back_button = await self.back_button()  # Создаем кнопку "Назад"
        title = await self.program_title(title="Отправка комментариев")
        await self.view_with_elements(title=title, buttons=[back_button], route_page="submitting_comments", lv=lv)
        page.update()  # Обновляем страницу

    async def change_name_description_photo(self, page: ft.Page):
        """Создает страницу Смена имени, описания, фото"""
        logger.info("Пользователь перешел на страницу Смена имени, описания, фото")
        page.views.clear()  # Очищаем страницу и добавляем новый View
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения информации
        back_button = await self.back_button()  # Создаем кнопку "Назад"
        title = await self.program_title(title="Смена имени, описания, фото")
        await self.view_with_elements(title=title, buttons=[back_button], route_page="change_name_description_photo",
                                      lv=lv)
        page.update()  # Обновляем страницу

    async def channel_subscription(self, page: ft.Page):
        """Создает страницу Подписка на каналы"""
        logger.info("Пользователь перешел на страницу Подписка на каналы")
        page.views.clear()  # Очищаем страницу и добавляем новый View
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения информации
        back_button = await self.back_button()  # Создаем кнопку "Назад"
        title = await self.program_title(title="Подписка на каналы")
        await self.view_with_elements(title=title, buttons=[back_button], route_page="channel_subscription", lv=lv)
        page.update()  # Обновляем страницу

    async def creating_list_of_channels(self, page: ft.Page):
        """Создает страницу Формирование списка каналов"""
        logger.info("Пользователь перешел на страницу Формирование списка каналов")
        page.views.clear()  # Очищаем страницу и добавляем новый View
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения информации
        back_button = await self.back_button()  # Создаем кнопку "Назад"
        title = await self.program_title(title="Формирование списка каналов")
        await self.view_with_elements(title=title, buttons=[back_button], route_page="creating_list_of_channels", lv=lv)
        page.update()  # Обновляем страницу

    async def documentation(self, page: ft.Page):
        """Создает страницу документации"""
        logger.info("Пользователь перешел на страницу документации")
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения информации
        page.views.clear()  # Очищаем страницу и добавляем новый View
        back_button = await self.back_button()  # Создаем кнопку "Назад"
        title = await self.program_title(title="Документация")
        await self.view_with_elements(title=title, buttons=[back_button], route_page="documentation", lv=lv)
        page.update()  # Обновляем страницу

    async def getting_list_channels(self, page: ft.Page):
        """Создает страницу Получение списка каналов"""
        logger.info("Пользователь перешел на страницу Получение списка каналов")
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения информации
        page.views.clear()  # Очищаем страницу и добавляем новый View

        async def action_1_with_log(_):
            try:
                lv.controls.append(ft.Text("Получение списка каналов..."))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
                config = await read_config()
                client = await connect_telegram_account(config.get("telegram_settings", "id"),
                                                        config.get("telegram_settings", "hash"))
                dialogs = await client.get_dialogs()
                username_diclist = await creating_a_channel_list(dialogs)  # Создаем или подключаемся к базе данных SQLite
                for username in username_diclist:
                    logger.info(username)
                    lv.controls.append(ft.Text(f"Найден канал: {username}"))  # отображаем сообщение в ListView
                    page.update()  # Обновляем страницу после каждого добавления
                await client.disconnect()  # Завершаем работу клиента
                lv.controls.append(ft.Text("Получение списка каналов завершено."))  # отображаем сообщение в ListView
                page.update()  # Обновляем страницу
            except Exception as e:
                logger.exception(e)
                lv.controls.append(ft.Text(f"Ошибка: {str(e)}"))  # отображаем ошибку в ListView
                page.update()  # Обновляем страницу

        # Создаем кнопку "Получение списка каналов"
        getting_list_channels_button = ft.ElevatedButton(
            "Получение списка каналов",  # Текст на кнопке
            on_click=action_1_with_log,  # Переход на главную страницу
            width=850,  # Ширина кнопки (увеличено для наглядности)
            height=35,  # Высота кнопки (увеличено для наглядности)
        )
        back_button = await self.back_button()  # Создаем кнопку "Назад"
        title = await self.program_title(title="Получение списка каналов")
        await self.view_with_elements(title=title, buttons=[getting_list_channels_button, back_button],
                                      route_page="getting_list_channels", lv=lv)
        page.update()  # Обновляем страницу

    async def program_title(self, title):
        """"Заголовок страниц программы"""
        # Создаем заголовок
        title = ft.Text(
            spans=[
                ft.TextSpan(
                    title,  # Текст заголовка
                    ft.TextStyle(
                        size=24,  # Размер заголовка
                        weight=self.TITLE_FONT_WEIGHT,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [self.PRIMARY_COLOR, self.PRIMARY_COLOR]
                            )), ), ), ], )
        return title

    async def back_button(self):
        """Кнопка назад."""
        # Создаем кнопку "Назад"
        back_button = ft.ElevatedButton(
            "Назад",  # Текст на кнопке
            on_click=lambda _: self.page.go("/"),  # Переход на главную страницу
            width=850,  # Ширина кнопки (увеличено для наглядности)
            height=35,  # Высота кнопки (увеличено для наглядности)
        )
        return back_button

    async def view_with_elements(self, title: ft.Text, buttons: list[ft.ElevatedButton], route_page, lv: ft.ListView):
        # Создаем View с элементами
        self.page.views.append(
            ft.View(
                f"/{route_page}",
                controls=[
                    ft.Column(
                        controls=[title, lv, *buttons],
                        expand=True,  # Растягиваем Column на всю доступную область
                    )],
                padding=20,  # Добавляем отступы вокруг содержимого
            ))

    async def main(self, page: ft.Page):
        """Точка входа в приложение."""
        self.page = page
        self.info_list = ft.ListView(expand=True, spacing=10, padding=self.PADDING, auto_scroll=True)
        await self.setup()


if __name__ == "__main__":
    ft.app(target=Application().main)
