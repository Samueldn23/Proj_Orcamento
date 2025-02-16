"""Módulo para o menu de orçamentos. base/orcamentos/menu_orc.py"""

from typing import Callable

import flet as ft

from src.core.orcamento import eletrica, fundacao, laje, paredes, telhado, contrapiso

from src.core.cliente import projetos
from src.core.orcamento.index_orcamento import criar_projeto

from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories.module_repository import ModuleRepository

gsm = get_style_manager()
module_repo = ModuleRepository()


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
        self.modulo = module_repo.get_modules(self.cliente["user_id"])
        self._init_buttons()

    def _init_buttons(self):
        """Inicializa os botões do menu"""
        self.menu_items = []
        # Certifique-se de que `self.modulo` é iterável
        if self.modulo:
            for modulo in self.modulo:
                if modulo.get(
                    "parede", False
                ):  # Verifica se o módulo tem `parede` = True
                    self.menu_items.append(
                        {
                            "text": "Parede",
                            "action": lambda _: paredes.mostrar_parede(
                                self.page, self.cliente
                            ),
                            "icon": "icons/parede.png",
                        }
                    )
                if modulo.get(
                    "contrapiso", False
                ):  # Verifica se o módulo tem `contrapiso` = True
                    self.menu_items.append(
                        {
                            "text": "Contrapiso",
                            "action": lambda _: contrapiso.mostrar_contrapiso(
                                self.page, self.cliente
                            ),
                            "icon": "icons/contrapiso.png",
                        }
                    )
                if modulo.get("laje", False):  # Verifica se o módulo tem `laje` = True
                    self.menu_items.append(
                        {
                            "text": "Laje",
                            "action": lambda _: laje.mostrar_laje(
                                self.page, self.cliente
                            ),
                            "icon": "icons/laje.png",
                        }
                    )
                if modulo.get(
                    "telhado", False
                ):  # Verifica se o módulo tem `telhado` = True
                    self.menu_items.append(
                        {
                            "text": "Telhado",
                            "action": lambda _: telhado.mostrar_telhado(
                                self.page, self.cliente
                            ),
                            "icon": "icons/telhado.png",
                        }
                    )
                if modulo.get(
                    "eletrica", False
                ):  # Verifica se o módulo tem `eletrica` = True
                    self.menu_items.append(
                        {
                            "text": "Elétrica",
                            "action": lambda _: eletrica.mostrar_eletrica(
                                self.page, self.cliente
                            ),
                            "icon": "icons/eletrica.png",
                        }
                    )
                if modulo.get(
                    "fundacao", False
                ):  # Verifica se o módulo tem `fundacao` = True
                    self.menu_items.append(
                        {
                            "text": "Fundação",
                            "action": lambda _: fundacao.mostrar_fundacao(
                                self.page, self.cliente
                            ),
                            "icon": "icons/fundacao.png",
                        }
                    )
                self.menu_items.append(
                    {
                        "text": "Orçamento",
                        "action": lambda _: criar_projeto(self.page, self.cliente),
                        "icon": "icons/icon.png",
                    }
                )

            # Cria os botões do menu
            # self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]
            self.menu_buttons = [
                self._create_menu_button(item) for item in self.menu_items
            ]

            # Botão voltar
            self.voltar_button = gsm.create_button(
                text="Voltar",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _, cliente=self.cliente: projetos.projetos_cliente(
                    self.page, cliente
                ),
                hover_color=gsm.colors.VOLTAR,
                width=130,
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
