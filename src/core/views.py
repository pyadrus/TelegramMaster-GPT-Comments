# -*- coding: utf-8 -*-
import flet as ft

TITLE_FONT_WEIGHT = ft.FontWeight.BOLD
PRIMARY_COLOR = ft.colors.CYAN_600


async def message_output_program_window(lv: ft.ListView, page: ft.Page, message_program):
    """
    Вывод сообщений в окно программы.
    :param lv: ListView
    :param page: Страница приложения.
    :param message_program: Сообщение.
    """
    lv.controls.append(ft.Text(f"{message_program}", color=ft.colors.RED))  # отображаем сообщение в ListView
    page.update()  # Обновляем страницу


async def view_with_elements_input_field(page: ft.Page, title: ft.Text, buttons: list[ft.ElevatedButton], route_page,
                                         lv: ft.ListView, text_field: ft.TextField):
    """
    Создаем View с элементами и добавляем в него элементы
    :param title: Текст заголовка
    :param buttons: Кнопки
    :param route_page: Название страницы
    :param lv: ListView
    :param text_field: TextField
    :param page: Страница приложения.
    """
    # Создаем View с элементами
    page.views.append(
        ft.View(
            f"/{route_page}",
            controls=[
                ft.Column(
                    controls=[title, lv, text_field, *buttons],
                    expand=True,  # Растягиваем Column на всю доступную область
                )],
            padding=20,  # Добавляем отступы вокруг содержимого
        ))


async def program_title(title):
    """"Заголовок страниц программы"""
    # Создаем заголовок
    title = ft.Text(
        spans=[
            ft.TextSpan(
                title,  # Текст заголовка
                ft.TextStyle(
                    size=24,  # Размер заголовка
                    weight=TITLE_FONT_WEIGHT,
                    foreground=ft.Paint(
                        gradient=ft.PaintLinearGradient(
                            (0, 20), (150, 20), [PRIMARY_COLOR, PRIMARY_COLOR]
                        )), ), ), ], )
    return title


async def view_with_elements(page: ft.Page, title: ft.Text, buttons: list[ft.ElevatedButton], route_page,
                             lv: ft.ListView,
                             content: list[ft.Control] = None):
    # Создаем View с элементами

    if content:
        lv.controls.extend(content)

    page.views.append(
        ft.View(
            f"/{route_page}",
            controls=[
                ft.Column(
                    controls=[title, lv, *buttons],
                    expand=True,  # Растягиваем Column на всю доступную область
                )],
            padding=20,  # Добавляем отступы вокруг содержимого
        ))
