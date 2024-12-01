"""Módulo para o menu de orçamentos. menu_orc.py"""

from typing import Callable

import flet as ft

from base.orcamentos import (
    contrapiso,
    eletrica,
    fundacao,
    laje,
    paredes,
    telhado,
)
from base.clientes import detalhes
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


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
                        color=gsm.colors.PRIMARY,
                    ),
                    ft.Text(text),
                ]
            ),
            on_click=on_click,
            width=width,
        )


class OrcamentoPage:
    """Classe para gerenciar a página de orçamentos"""

    def __init__(self, page: ft.Page, _cliente):
        self.page = page
        self.cliente = _cliente
        self._init_buttons()

    def _init_buttons(self):
        """Inicializa os botões do menu"""
        self.menu_items = [
            {
                "text": "Parede",
                "action": lambda _: [
                    paredes.mostrar_parede(self.page, self.cliente),
                ],
                "icon": "icons/parede.png",
            },
            {
                "text": "Elétrica",
                "action": lambda _: eletrica.mostrar_eletrica(self.page),
                "icon": "icons/eletrica.png",
            },
            {
                "text": "Laje",
                "action": lambda _: laje.mostrar_laje(self.page),
                "icon": "icons/laje.png",
            },
            {
                "text": "Contrapiso",
                "action": lambda _: contrapiso.mostrar_contrapiso(self.page),
                "icon": "icons/contrapiso.png",
            },
            {
                "text": "Fundação",
                "action": lambda _: fundacao.mostrar_fundacao(self.page),
                "icon": "assets/img/iconFundacao.png",
            },
            {
                "text": "Telhado",
                "action": lambda _: telhado.mostrar_telhado(self.page),
                "icon": "icons/telhado.png",
            },
        ]

        # Cria os botões do menu
        # self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]
        self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

        # Botão voltar
        self.voltar_button = gsm.create_button(
            text="Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda _, cliente=self.cliente: detalhes.detalhes_cliente(
                self.page, cliente
            ),
            hover_color=gsm.colors.VOLTAR,
        )

    def _create_menu_button(self, item: dict) -> ft.Container:
        """Cria um botão de menu estilizado"""
        return gsm.create_button_custom(
            text=item["text"],
            icon=item["icon"],
            on_click=lambda _: item["action"](self.page),
            width=200,
        )

    def build(self):
        """Constrói a interface da página de orçamentos"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"Novo Orçamentos para o cliente {self.cliente['nome']}",
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
                    ft.Divider(height=20),
                    self.voltar_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.all(20),
            alignment=ft.alignment.top_center,
        )


def mostrar_orcamento(page: ft.Page, _cliente):
    """Função helper para mostrar a página de orçamentos"""
    page.controls.clear()
    orcamento_page = OrcamentoPage(page, _cliente)
    page.add(orcamento_page.build())
    page.update()
