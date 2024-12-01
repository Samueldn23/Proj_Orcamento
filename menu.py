"""Importações necessárias para o funcionamento do menu principal. menu.py"""

from typing import Callable

import flet as ft

from models.db import Usuario

from App.Clientes import clientes, empresa
from App.orcamentos import menu_orc
from custom.styles_utils import get_style_manager
from examples import exemplos
from tests import teste_btn

gsm = get_style_manager()


class MenuButton(ft.ElevatedButton):
    """Classe personalizada para botões do menu principal"""

    def __init__(self, text: str, on_click: Callable, width: int = 200):
        super().__init__(
            text=text,
            on_click=on_click,
            width=width,
        )


class MenuPrincipalPage:
    """Classe para gerenciar a página do menu principal"""

    def __init__(self, page: ft.Page):
        self.page = page
        self._init_buttons()

    def _init_buttons(self):
        """Inicializa os botões do menu principal"""
        self.menu_items = [
            {
                "text": " Clientes",
                "action": clientes.tela_clientes,
            },
            {
                "text": "Orçamentos",
                "action": menu_orc.mostrar_orcamento,
            },
            {
                "text": "Cadastro de Clientes",
                "action": cadastro.tela_cadastro_cliente,
            },
            {
                "text": "cadastrar empresa",
                "action": empresa.tela_cadastro_empresa,
            },
            {
                "text": "Exemplo",
                "action": exemplos.main,
            },
            {
                "text": "Teste Butões",
                "action": teste_btn.main,
            },
        ]

        # Cria os botões do menu
        self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

    def _create_menu_button(self, item: dict) -> ft.Container:
        """Cria um botão de menu estilizado"""
        return gsm.create_button(
            text=item["text"],
            on_click=lambda _: item["action"](self.page),
            width=200,
            hover_color=ft.Colors.PURPLE,
            text_color=ft.Colors.ORANGE,
        )

    def build(self):
        """Constrói a interface da página do menu principal"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Menu Principal",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE,
                    ),
                    ft.Divider(height=20, color=ft.Colors.BLUE_GREY_100),
                    ft.Row(
                        controls=self.menu_buttons,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Divider(height=20, color=ft.Colors.BLUE_GREY_100),
                    gsm.create_button(
                        "Sair",
                        on_click=lambda _: Usuario.deslogar(self.page),
                        width=100,
                        icon=ft.Icons.LOGOUT,
                        hover_color=ft.Colors.RED,
                        text_color=ft.Colors.WHITE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.all(20),
            alignment=ft.alignment.top_center,
        )


def mostrar_menu(page: ft.Page):
    """Função para mostrar a página do menu principal"""
    page.controls.clear()
    menu_principal_page = MenuPrincipalPage(page)
    page.add(menu_principal_page.build())
    page.update()
