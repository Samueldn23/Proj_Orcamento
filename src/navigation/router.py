"""Gerenciador de navegação entre telas"""

import flet as ft


def navigate_to_login(page: ft.Page):
    """Navega para a tela de login"""
    print("Navegando para a tela de login...")
    page.controls.clear()
    page.update()

    # Importação dinâmica para evitar circular import
    from src.user.login import mostrar_tela

    mostrar_tela(page)
    print("Tela de login carregada")


def navegar_para_menu(page: ft.Page):
    """Navega para o menu principal"""
    # Importação dinâmica
    from menu import mostrar_menu

    mostrar_menu(page)


def navegar_orcamento(page: ft.Page, cliente: dict, projeto: any):
    """Navega para o menu orcamento"""
    # Importação dinâmica
    from src.core.orcamento.listar_construcoes import mostrar_orcamento

    mostrar_orcamento(page, cliente, projeto)


def navegar_principal(page: ft.Page):
    """Voltar para o menu principal"""
    # Importação dinâmica
    from menu import mostrar_menu

    mostrar_menu(page)
