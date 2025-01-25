import flet as ft


async def create_buttons(text: str, on_click, width: int = 850, height: int = 35) -> ft.ElevatedButton:
    """
    Создает универсальную кнопку с заданными параметрами.

    :param text: Текст на кнопке.
    :param on_click: Функция, вызываемая при нажатии на кнопку.
    :param width: Ширина кнопки (по умолчанию 850).
    :param height: Высота кнопки (по умолчанию 35).
    :return: Объект кнопки ft.ElevatedButton.
    """
    return ft.ElevatedButton(text=text, on_click=on_click, width=width, height=height, )
