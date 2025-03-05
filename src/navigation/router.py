"""Gerenciador de navegação entre telas"""

import flet as ft


def navigate_to_login(page: ft.Page):
    """Navega para a tela de login"""
    print("Navegando para a tela de login...")

    # Limpa completamente a página antes de carregar a tela de login
    page.controls.clear()
    page.update()

    from src.user.login import mostrar_tela

    mostrar_tela(page)
    print("Tela de login carregada")


def navigate_to_menu(page: ft.Page):
    """Navega para o menu principal"""
    from menu import mostrar_menu

    mostrar_menu(page)


def navegar_orcamento(page, cliente, projeto):
    """Navega para o menu orcamento"""
    from src.core.orcamento.menu_orc import mostrar_orcamento

    mostrar_orcamento(page, cliente, projeto)


def navegar_principal(page):
    """Voltar para o menu principal"""
    from menu import mostrar_menu

    mostrar_menu(page)
