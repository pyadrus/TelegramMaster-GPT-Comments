import flet as ft
from loguru import logger

from src.core.configs import config
from src.core.getting_list_channels import ApplicationGettingListChannels
from src.core.logging_in import loging
from src.core.main_menu import MainMenu, actions_with_the_program_window

# Настройка логирования
logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")


class Application:
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
                "TelegramMaster Commentator 🚀\n\nTelegramMaster Commentator - это программа для автоматической расставления комментариев в каналах Telegram, а также для работы с аккаунтами. 💬\n\n"
                "📂 Проект доступен на GitHub: https://github.com/pyadrus/TelegramMaster_Commentator \n"
                "📲 Контакт с разработчиком в Telegram: https://t.me/PyAdminRU\n"
                f"📡 Информация на канале: https://t.me/master_tg_d"
            )
        )

        # Создаем главное меню
        self.menu = MainMenu(page, self.info_list).build()

        # Инициализация начального маршрута
        await self.route_change(None)

    async def route_change(self, route):
        """Обработчик изменения маршрута."""
        self.page.views.clear()

        # Основной макет (боковое меню и информационная панель)
        layout = ft.Row(
            [
                ft.Container(self.menu, width=config.PROGRAM_MENU_WIDTH, padding=config.PADDING),
                ft.Container(width=config.LINE_WIDTH, bgcolor=config.LINE_COLOR),  # Вертикальная линия
                ft.Container(self.info_list, expand=True, padding=config.PADDING),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,  # Убираем промежуток между элементами
            expand=True,
        )

        # Добавляем макет на страницу
        self.page.views.append(ft.View("/", [layout]))

        # Обработка маршрутов
        if self.page.route == "/getting_list_channels":  # 📋 Получение списка каналов
            logger.info("Получение списка каналов")
            app_getting_list = ApplicationGettingListChannels()
            await app_getting_list.setup(self.page)
        elif self.page.route == "/submitting_comments":  # 💬 Отправка комментариев
            logger.info("Отправка комментариев")
        elif self.page.route == "/change_name_description_photo":  # 🖼️ Смена имени, описания, фото
            logger.info("Смена имени, описания, фото")
        elif self.page.route == "/channel_subscription":  # 🔗 Подписка на каналы
            logger.info("Подписка на каналы")
        elif self.page.route == "/creating_list_of_channels":  # 📂 Формирование списка каналов
            logger.info("Формирование списка каналов")
        elif self.page.route == "/documentation":  # 📖 Документация
            logger.info("Документация")

        elif self.page.route == "/errors":
            # Пустая страница с уведомлением
            logger.info("Ошибка")
        self.page.update()

    async def main(self, page: ft.Page):
        """Точка входа в приложение."""
        await self.setup(page)


if __name__ == "__main__":
    app = Application()
    ft.app(target=app.main)
