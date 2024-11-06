import flet as ft
import custom.styles as stl
from App.orcamentos import menu_orc
from tests.teste import pageteste
from typing import Callable
from examples import exemplos, exemplo1


class MenuButton(ft.ElevatedButton):
    """Classe personalizada para botões do menu principal"""

    def __init__(self, text: str, on_click: Callable, width: int = 200):
        super().__init__(
            text=text,
            on_click=on_click,
            width=width,
            on_hover=stl.hover_effect_prinicipal,
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
                "text": "Orçamentos",
                "action": menu_orc.mostrar_orcamento,
            },
            {
                "text": "Exemplo 1",
                "action": exemplos.exemplo,
            },
            {
                "text": "Exemplo 2",
                "action": exemplo1.mostrar_exemplo,
            },
            {
                "text": "Teste",
                "action": pageteste,
            },
        ]

        # Cria os botões do menu
        self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

    def _create_menu_button(self, item: dict) -> ft.Container:
        """Cria um botão de menu estilizado"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    MenuButton(
                        text=item["text"],
                        on_click=lambda _: item["action"](self.page),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=2,
            border_radius=25,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: self._handle_button_hover(e),
        )

    def _handle_button_hover(self, e):
        """Gerencia o efeito hover nos botões"""
        if e.data == "true":  # Mouse entrou
            e.control.scale = 1.05
            e.control.shadow = ft.BoxShadow(
                #spread_radius=1,
                blur_radius=15,
                color=ft.colors.PURPLE_500,
                offset=ft.Offset(0, 0),
            )
        else:  # Mouse saiu
            e.control.scale = 1.0
            e.control.shadow = None
        e.control.update()

    def build(self):
        """Constrói a interface da página do menu principal"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Menu Principal",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE,
                    ),
                    ft.Divider(height=20, color=ft.colors.BLUE_GREY_100),
                    ft.Row(
                        controls=self.menu_buttons,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Divider(height=20, color=ft.colors.BLUE_GREY_100),
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
