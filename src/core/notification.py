# -*- coding: utf-8 -*-
import flet as ft  # Импортируем библиотеку flet


async def show_notification(page: ft.Page, message: str):
    """
    Функция для показа уведомления

    :param page: Страница интерфейса Flet для отображения элементов управления.
    :param message: Текст уведомления.
    """
    # Переход обратно после закрытия диалога
    dlg = ft.AlertDialog(title=ft.Text(message), on_dismiss=lambda e: page.go("/"))
    page.overlay.append(dlg)
    dlg.open = True
    page.update()
