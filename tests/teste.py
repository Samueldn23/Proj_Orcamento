"""Importação de bibliotecas e módulos necessários"""

import flet as ft

from custom.button import Voltar
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


def main(page: ft.Page):
    """Função principal do aplicativo"""
    # Definir os temas e estilos da aplicação
    page.controls.clear()
    page.title = "Aplicativo de Orçamento para Construção"

    btn_voltar = gsm.create_button(
        text="Voltar",
        on_click=lambda _: Voltar.principal(page),
        icon=ft.icons.ARROW_BACK_IOS_NEW,
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
            icon_color=ft.colors.BLUE,
            hover_icon_color=ft.colors.WHITE,
            hover_color=ft.colors.AMBER,
        ),
    )


# ft.app(target=main)
