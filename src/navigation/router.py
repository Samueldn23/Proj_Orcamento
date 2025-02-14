"""Gerenciador de navegação entre telas"""

import flet as ft


def navigate_to_login(page: ft.Page):
    """Navega para a tela de login"""
    from src.user.login import mostrar_tela

    mostrar_tela(page)


def navigate_to_menu(page: ft.Page):
    """Navega para o menu principal"""
    from menu import mostrar_menu

    mostrar_menu(page)
