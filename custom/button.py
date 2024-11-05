# Arquivo utils.py para armazenar funções auxiliares que se repetem em varias partes do código
from App.orcamentos import menu_orc
import menu


class voltar:
    def orcamento(page):
        page.controls.clear()
        menu_orc.mostrar_orcamento(page)

    def principal(page):
        page.controls.clear()
        menu.mostrar_menu(page)
