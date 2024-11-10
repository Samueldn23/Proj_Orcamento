import flet as ft
from typing import Callable
import App.orcamentos as orc
import custom.styles as stl
import custom.button as btn
from App.orcamentos import paredes


class MenuButton(ft.ElevatedButton):
    """Classe personalizada para botões do menu de orçamento"""

    def __init__(self, text: str, on_click: Callable, icon: str, width: int = 200):
        super().__init__(
            content=ft.Row(
                [
                    ft.Image(
                        src=icon,
                        width=22,
                        height=22,
                        color=ft.colors.WHITE,
                    ),
                    ft.Text(text)
                ]
            ),
            on_click=on_click,
            width=width,
            on_hover=stl.hover_effect,
        )


class OrcamentoPage:
    """Classe para gerenciar a página de orçamentos"""

    def __init__(self, page: ft.Page):
        self.page = page
        self._init_buttons()

    def _init_buttons(self):
        """Inicializa os botões do menu"""
        self.menu_items = [
            {
                "text": "Parede",
                "action": lambda _: paredes.mostrar_parede(self.page),
                "icon": "icons/parede.png", 
            },
            {
                "text": "Elétrica",
                "action": lambda _: orc.eletrica.mostrar_eletrica(self.page),
                "icon": "icons/eletrica.png",
            },
            {
                "text": "Laje",
                "action": lambda _: orc.laje.mostrar_laje(self.page),
                "icon": ft.icons.LAYERS,
            },
            {
                "text": "Contrapiso",
                "action": lambda _: orc.contrapiso.mostrar_contrapiso(self.page),
                "icon": ft.icons.FOUNDATION_SHARP,
            },
            {
                "text": "Fundação",
                "action": lambda _: orc.fundacao.mostrar_fundacao(self.page),
                "icon": 'assets/img/iconFundacao.png',  
            },
            {
                "text": "Telhado",
                "action": lambda _: orc.telhado.mostrar_telhado(self.page),
                "icon": "icons/telhado.png",
            },
        ]

        # Cria os botões do menu
        self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

        # Botão voltar
        self.voltar_button = ft.ElevatedButton(
            text="Voltar",
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: btn.voltar.principal(self.page),
            on_hover=stl.hover_effect_voltar,
            style=ft.ButtonStyle(
                color=ft.colors.BLUE_900,
            ),
        )

    def _create_menu_button(self, item: dict) -> ft.Container:
        """Cria um botão de menu estilizado"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    MenuButton(
                        text=item["text"],
                        icon=item["icon"],
                        on_click=lambda _: item["action"](self.page),
                        width=150,
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
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_500,
                offset=ft.Offset(0, 0),
            )
        else:  # Mouse saiu
            e.control.scale = 1.0
            e.control.shadow = None
        e.control.update()

    def build(self):
        """Constrói a interface da página de orçamentos"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Menu de Orçamentos",
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
                    ft.Divider(height=20),
                    self.voltar_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.all(20),
            alignment=ft.alignment.top_center,
        )


def mostrar_orcamento(page: ft.Page):
    """Função helper para mostrar a página de orçamentos"""
    page.controls.clear()
    orcamento_page = OrcamentoPage(page)
    page.add(orcamento_page.build())
    page.update()
