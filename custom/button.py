"""Arquivo utils.py para armazenar funções auxiliares que se repetem em varias partes do código"""

import menu
from App.orcamentos import menu_orc


class Voltar:
    """Classe para voltar para a página anterior."""

    def __init__(self, controls):
        self.controls = controls  # Atribuindo controls ao objeto

    def orcamento(self, page):
        """Voltar para a página de orçamentos."""
        page.controls.clear()
        menu_orc.mostrar_orcamento(page)

    def principal(self, page):
        """ "Voltar para a página principal."""
        page.controls.clear()
        menu.mostrar_menu(page)
