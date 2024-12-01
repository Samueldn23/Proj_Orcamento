"""Importação de bibliotecas e módulos necessários"""

import flet as ft

from custom.button import Voltar
from custom.styles_utils import get_style_manager
from user import login
from models.db import Usuario

gsm = get_style_manager()


def main(page: ft.Page):
    """Função principal do aplicativo"""
    # Definir os temas e estilos da aplicação
    page.controls.clear()
    page.title = "Aplicativo de Orçamento para Construção"

    btn_voltar = gsm.create_button(
        text="Voltar",
        on_click=lambda _: Voltar.principal(page),
        icon=ft.Icons.ARROW_BACK_IOS_NEW,
        hover_color=gsm.colors.VOLTAR,
    )

    page.add(
        btn_voltar,
        ft.Divider(),
        gsm.create_button_custom(
            text="teste 3",
            on_click=lambda _: print("teste 3"),
            icon="icons/eletrica.png",
        ),
        gsm.create_button_custom(
            text="teste 4",
            on_click=lambda _: print("teste 4"),
            icon="icons/eletrica.png",
            width=150,
            icon_color=ft.Colors.BLUE,
            hover_icon_color=ft.Colors.WHITE,
            hover_color=ft.Colors.AMBER,
        ),
        gsm.create_button(
            text="tela de login",
            on_click=lambda _: login.mostrar_tela(page),
            icon=ft.Icons.ADD,
            icon_color=ft.Colors.BLUE,
            hover_icon_color=ft.Colors.WHITE,
            hover_color=ft.Colors.AMBER,
        ),
        ft.Divider(),
        gsm.create_button(
            text="Deslogar",
            on_click=lambda _: Usuario.deslogar(page),
            icon=ft.Icons.LOGOUT,
            hover_color=gsm.colors.VOLTAR,
        ),
        gsm.create_button(
            text="",
            on_click=lambda _: print("teste 5"),
            icon=ft.Icons.ADD,
            icon_color=ft.Colors.BLUE,
            hover_icon_color=ft.Colors.WHITE,
            hover_color=ft.Colors.AMBER,
            width=70,
        ),
        gsm.create_icon_button(
            icon=ft.Icons.ADD,
            on_click=lambda _: print("teste 6"),
            icon_color=ft.Colors.BLUE,
            # hover_icon_color=ft.Colors.WHITE,
            hover_color=ft.Colors.AMBER,
        ),
    )


# ft.app(target=main)
