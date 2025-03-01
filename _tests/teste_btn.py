"""Importação de bibliotecas e módulos necessários"""

import flet as ft

from src.custom.styles_utils import get_style_manager
from src.navigation.router import navegar_principal

gsm = get_style_manager()


def main(page: ft.Page):
    """Função principal do aplicativo"""
    # Definir os temas e estilos da aplicação
    page.controls.clear()
    page.title = "Aplicativo de Orçamento para Construção"

    btn_voltar = gsm.create_button(
        text="Voltar",
        on_click=lambda _: navegar_principal(page),
        icon=ft.Icons.ARROW_BACK_IOS_NEW,
        hover_color=gsm.colors.VOLTAR,
        width=130,
    )

    page.add(
        btn_voltar,
        gsm.create_button(
            text="Teste 1",
            on_click=lambda _: print("Botão 1 pressionado"),
            width=230,
            hover_color="#0BF1F1",
            icon=ft.Icons.CALCULATE,
        ),
        ft.ElevatedButton(
            text="teste",
            icon=ft.Icons.CALCULATE,
            on_click=lambda _: print("teste"),
        ),
        gsm.create_button(
            text="Calcular",
            icon=ft.Icons.CALCULATE,
            on_click=lambda _: print("Botão 1 pressionado"),
            width=130,
            hover_color=ft.Colors.BLUE_600,
        ),
    )


# ft.app(target=main)
