import flet as ft
from loguru import logger

from src.core.configs import config
from src.gui.base_application import BaseApplication


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


class ApplicationGettingListChannels(BaseApplication):
    """Класс для управления приложением. 📋 Получение списка каналов"""

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

    async def route_change(self, route):
        """Обработчик изменения маршрута."""
        await super().route_change(route)

        if self.page.route == "/getting_list_channels":  # 📋 Получение списка каналов
            logger.info("Получение списка каналов")
            # Очищаем info_list и добавляем новое сообщение
            self.info_list.controls.clear()
            self.info_list.controls.append(
                ft.Text(
                    "Получение списка каналов\n\n"
                )
            )
        elif self.page.route == "/":  # Главная страница
            logger.info("Главная страница")
            # Очищаем info_list и добавляем стартовое сообщение
            self.info_list.controls.clear()
            self.info_list.controls.append(
                ft.Text(
                    "TelegramMaster Commentator 🚀\n\nTelegramMaster Commentator - это программа для автоматической "
                    "расставления комментариев в каналах Telegram, а также для работы с аккаунтами. 💬\n\n"
                    "📂 Проект доступен на GitHub: https://github.com/pyadrus/TelegramMaster_Commentator \n"
                    "📲 Контакт с разработчиком в Telegram: https://t.me/PyAdminRU\n"
                    f"📡 Информация на канале: https://t.me/master_tg_d"
                )
            )

        self.page.update()