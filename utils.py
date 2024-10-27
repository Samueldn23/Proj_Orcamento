# Arquivo para armazenar funções auxiliares que se repetem em varias partes do código

from orcamentos import menu_orc

class voltar:
    def orcamento(page):
        page.controls.clear()
        menu_orc.orcamento(page) 
