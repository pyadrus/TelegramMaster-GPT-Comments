import flet as ft
from loguru import logger
from src.core.logging_in import loging
from src.gui.app import action_1_with_log, action_2_with_log, action_3, action_4, action_5
from src.core.configs import program_version, date_of_program_change

logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")  # Логирование программы


async def show_author_info(page: ft.Page):
    """Отображает информацию об авторе."""
    page.show_snack_bar(
        ft.SnackBar(
            ft.Text(f"Разработчик: Ваше имя\nВерсия программы: {program_version}"),
            duration=3000,
        )
    )


async def display_settings(page: ft.Page):
    """Обновляет содержимое окна для отображения настроек."""
    page.clean()
    page.add(
        ft.Text("Настройки программы", style="headlineMedium"),
        ft.ElevatedButton(text="Назад", on_click=lambda _: display_main_menu(page))
    )


async def display_main_menu(page: ft.Page):
    """Обновляет содержимое окна для отображения основного меню."""
    page.clean()

    info_field = ft.TextField(read_only=True, multiline=True, width=350, height=300)

    btn_1 = ft.ElevatedButton(text="Получение списка каналов", on_click=lambda _: action_1_with_log(info_field))
    btn_2 = ft.ElevatedButton(text="Отправка комментариев", on_click=lambda _: action_2_with_log(info_field))
    btn_3 = ft.ElevatedButton(text="Смена имени, описания, фото", on_click=lambda _: action_3(info_field))
    btn_4 = ft.ElevatedButton(text="Подписка на каналы", on_click=lambda _: action_4(info_field))
    btn_5 = ft.ElevatedButton(text="Формирование списка каналов", on_click=lambda _: action_5(info_field))

    page.add(
        ft.Column(
            [
                ft.Row([btn_1], alignment=ft.MainAxisAlignment.START),
                ft.Row([btn_2], alignment=ft.MainAxisAlignment.START),
                ft.Row([btn_3], alignment=ft.MainAxisAlignment.START),
                ft.Row([btn_4], alignment=ft.MainAxisAlignment.START),
                ft.Row([btn_5], alignment=ft.MainAxisAlignment.START),
                ft.Row([info_field], alignment=ft.MainAxisAlignment.END)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )
    )


async def main(page: ft.Page):
    await loging()

    page.title = f"Версия {program_version}. Дата изменения {date_of_program_change}"
    page.window_width = 720
    page.window_height = 400

    def handle_menu_item_click(e: ft.ControlEvent):
        if e.control.text == "Автор":
            show_author_info(page)
        elif e.control.text == "Настройки":
            display_settings(page)
        elif e.control.text == "Выход":
            page.window_close()

    menu_items = [
        ft.PopupMenuItem(text="Автор", on_click=handle_menu_item_click),
        ft.PopupMenuItem(text="Настройки", on_click=handle_menu_item_click),
        ft.PopupMenuItem(),  # Разделитель
        ft.PopupMenuItem(text="Выход", on_click=handle_menu_item_click),
    ]

    page.menu = ft.PopupMenuButton(items=menu_items)

    await display_main_menu(page)


if __name__ == "__main__":
    ft.app(target=main)
