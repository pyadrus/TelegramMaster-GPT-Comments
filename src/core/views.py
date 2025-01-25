import flet as ft

TITLE_FONT_WEIGHT = ft.FontWeight.BOLD
PRIMARY_COLOR = ft.colors.CYAN_600

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


async def view_with_elements(page, title: ft.Text, buttons: list[ft.ElevatedButton], route_page, lv: ft.ListView):
    # Создаем View с элементами
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