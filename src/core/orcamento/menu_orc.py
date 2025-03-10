"""Módulo para o menu de orçamentos. base/orcamentos/menu_orc.py"""

from collections.abc import Callable

import flet as ft

# Importações diretas das funções mostrar_
from src.core.orcamento.contrapiso import mostrar_contrapiso
from src.core.orcamento.eletrica import mostrar_eletrica
from src.core.orcamento.fundacao import mostrar_fundacao
from src.core.orcamento.laje import mostrar_laje
from src.core.orcamento.paredes import mostrar_parede
from src.core.orcamento.telhado import mostrar_telhado
from src.core.projeto.detalhes_projeto import tela_detalhes_projeto
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories.module_repository import ModuleRepository as RepositorioModulo

gsm = get_style_manager()
repositorio_modulo = RepositorioModulo()


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
    """Classe para a página de orçamentos"""

    def __init__(self, page: ft.Page, _cliente, projeto):
        self.page = page
        self.cliente = _cliente
        self.projeto = projeto
        self.modulo = repositorio_modulo.get_modules(self.cliente["user_id"])
        self.menu_buttons = []  # Inicializa a lista de botões vazia

        # Inicializa o botão voltar
        self.voltar_button = gsm.create_button(
            text="Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda _: tela_detalhes_projeto(self.page, self.projeto, self.cliente),
            hover_color=gsm.colors.VOLTAR,
            width=130,
        )

        self._init_buttons()

    def _init_buttons(self):
        """Inicializa os botões do menu"""
        self.menu_items = []
        # Certifique-se de que `self.modulo` é iterável
        if self.modulo:
            for modulo in self.modulo:
                if modulo.get("parede", False):  # Verifica se o módulo tem `parede` = True
                    self.menu_items.append(
                        {
                            "text": "Parede",
                            "action": lambda _: mostrar_parede(self.page, self.cliente, self.projeto),
                            "icon": "icons/parede.png",
                        }
                    )
                if modulo.get("contrapiso", False):  # Verifica se o módulo tem `contrapiso` = True
                    self.menu_items.append(
                        {
                            "text": "Contrapiso",
                            "action": lambda _: mostrar_contrapiso(self.page, self.cliente, self.projeto),
                            "icon": "icons/contrapiso.png",
                        }
                    )
                if modulo.get("laje", False):  # Verifica se o módulo tem `laje` = True
                    self.menu_items.append(
                        {
                            "text": "Laje",
                            "action": lambda _: mostrar_laje(self.page, self.cliente, self.projeto),
                            "icon": "icons/laje.png",
                        }
                    )
                if modulo.get("telhado", False):  # Verifica se o módulo tem `telhado` = True
                    self.menu_items.append(
                        {
                            "text": "Telhado",
                            "action": lambda _: mostrar_telhado(self.page, self.cliente, self.projeto),
                            "icon": "icons/telhado.png",
                        }
                    )
                if modulo.get("eletrica", False):  # Verifica se o módulo tem `eletrica` = True
                    self.menu_items.append(
                        {
                            "text": "Elétrica",
                            "action": lambda _: mostrar_eletrica(self.page, self.cliente, self.projeto),
                            "icon": "icons/eletrica.png",
                        }
                    )
                if modulo.get("fundacao", False):  # Verifica se o módulo tem `fundacao` = True
                    self.menu_items.append(
                        {
                            "text": "Fundação",
                            "action": lambda _: mostrar_fundacao(self.page, self.cliente, self.projeto),
                            "icon": "icons/fundacao.png",
                        }
                    )

            # Cria os botões do menu
            self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

    def _create_menu_button(self, item: dict) -> ft.Container:
        """Cria um botão de menu estilizado"""
        return gsm.create_button_custom(
            text=item["text"],
            icon=item["icon"],
            on_click=lambda _: item["action"](self.page),
            width=200,
        )

    def build(self):
        """Constrói a página de orçamentos"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Orçamento de Construção",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE,
                                text_align=ft.TextAlign.CENTER,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"Projeto: {self.projeto.nome}",
                                size=18,
                                color=ft.Colors.BLUE_GREY,
                                text_align=ft.TextAlign.CENTER,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
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
                spacing=10,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )


def mostrar_orcamento(page: ft.Page, _cliente, projeto):
    """Função helper para mostrar a página de orçamentos"""
    page.controls.clear()
    orcamento_page = OrcamentoPage(page, _cliente, projeto)
    page.add(orcamento_page.build())
    page.update()
