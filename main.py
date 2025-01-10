import flet as ft
from loguru import logger
from src.core.configs import program_version, date_of_program_change, program_name
from src.core.logging_in import loging
from src.gui.app import action_1_with_log, action_2_with_log, action_3, action_4, action_5

logger.add("user_data/log/log.log", rotation="1 MB", compression="zip")  # Логирование программы

window_width = 535  # ширина
window_height = 600  # высота
name = "MenuBar Example"


async def display_main_menu(page):
    """Создает список кнопок для основного меню."""
    button_width = 500  # ширина
    button_height = 80  # высота
    buttons = [
        ft.ElevatedButton(text="Получение списка каналов", on_click=lambda _: action_1_with_log(page),
                          width=button_width, height=button_height),
        ft.ElevatedButton(text="Отправка комментариев", on_click=lambda _: action_2_with_log(page),
                          width=button_width, height=button_height),
        ft.ElevatedButton(text="Смена имени, описания, фото", on_click=lambda _: action_3(page),
                          width=button_width, height=button_height),
        ft.ElevatedButton(text="Подписка на каналы", on_click=lambda _: action_4(page),
                          width=button_width, height=button_height),
        ft.ElevatedButton(text="Формирование списка каналов", on_click=lambda _: action_5(page),
                          width=button_width, height=button_height),
    ]
    return ft.Column(
        [
            ft.Row([btn]) for btn in buttons
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=50,  # расстояние между кнопками
        expand=True
    )


def example():
    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")

    menubar = ft.MenuBar( style=ft.MenuStyle(
        alignment=ft.alignment.top_left,
            bgcolor=ft.colors.RED_100,
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            ft.SubmenuButton(content=ft.Text("Документация"), controls=[
                ft.MenuItemButton(content=ft.Text("Документация"), on_click=handle_menu_item_click, ), ], ),
            ft.SubmenuButton(content=ft.Text("Настройки"), controls=[
                ft.MenuItemButton(content=ft.Text("Настройки"), on_click=handle_menu_item_click, ), ], ),
            ft.SubmenuButton(content=ft.Text("Выключить"), controls=[
                ft.MenuItemButton(content=ft.Text("Выключить"), on_click=handle_menu_item_click, ), ], ),
            ft.SubmenuButton(content=ft.Text("Об программе"), controls=[
                ft.MenuItemButton(content=ft.Text("Об программе"), on_click=handle_menu_item_click, ), ], ),
        ], )
    return ft.Row([menubar])


async def main(page: ft.Page):
    await loging()
    page.title = f"Версия {program_version}. Дата изменения {date_of_program_change}"
    page.window.width = window_width  # Ширина окна
    page.window.height = window_height  # Высота окна

    # Создаем основной контейнер для страницы
    main_container = ft.Column()

    # Добавляем текстовый элемент в контейнер
    t = ft.Text(
        spans=[
            ft.TextSpan(
                program_name,
                ft.TextStyle(
                    size=30,
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
    main_container.controls.append(t)

    # Добавляем кнопки в контейнер
    menu = await display_main_menu(page)
    main_container.controls.append(menu)

    # Добавьте строку меню на страницу
    page.appbar = example()

    # Обновляем содержимое страницы
    page.add(main_container)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
