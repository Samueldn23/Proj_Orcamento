"""Importações necessárias para o funcionamento do menu principal. menu.py"""

# 1. Módulos padrão
from typing import Callable

# 2. Módulos de terceiros
import flet as ft

# 3. Módulos locais
from src.core.cliente import clientes
from src.core.empresa import empresa

# from base.SPDA import SPDA
from src.core.configuracao import configuracao
from examples import exemplos
from src.infrastructure.database.repositories import UserRepository
from tests import teste_btn
from src.custom.styles_utils import get_style_manager
from src.navigation.router import navigate_to_login  # Nova importação

gsm = get_style_manager()
Usuario = UserRepository()  # Instanciar o repositório


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
                "text": "Empresa",
                "action": empresa.tela_cadastro_empresa,
            },
            {
                "text": "Exemplo",
                "action": exemplos.mostrar_parede,
            },
            {
                "text": "Teste Butões",
                "action": teste_btn.main,
            },
            {
                "text": "Configuração",
                "action": configuracao.tela_config,
            },
        ]

        # Cria os botões do menu
        self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

    def _handle_logout(self, _):
        """Função para lidar com o logout"""
        if Usuario.logout():
            # Se o logout foi bem sucedido, volta para a tela de login
            navigate_to_login(self.page)
        else:
            # Se houve erro, mostra mensagem
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Erro ao realizar logout!"), bgcolor=ft.colors.ERROR
                )
            )

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
                        on_click=self._handle_logout,  # Usar o novo método
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
