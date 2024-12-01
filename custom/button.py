"""Arquivo utils.py para armazenar funções auxiliares que se repetem em varias partes do código"""

from base.orcamentos import menu_orc


class Voltar:
    """Classe para voltar para a página anterior."""

    def __init__(self, controls):
        self.controls = controls  # Atribuindo controls ao objeto

    def orcamento(page, cliente):  # pylint: disable=E0213
        """Voltar para a página de orçamentos."""
        page.controls.clear()
        menu_orc.mostrar_orcamento(page, cliente)

    def principal(page):  # pylint: disable=E0213
        """ "Voltar para a página principal."""
        from menu import mostrar_menu

        page.controls.clear()
        mostrar_menu(page)
