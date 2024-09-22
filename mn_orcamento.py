import flet as ft
from orc_paredes import mostrar_parede  # Importa a função mostrar_parede
from orc_eletrica import mostrar_eletrica  # Importa a função mostrar_eletrica

def orcamento(page):
    page.controls.clear()
    page.add(ft.Text("Tela de Orçamento", size=24))

    btn_parede = ft.ElevatedButton(text="Parede", on_click=lambda e: mostrar_parede(page), width=200)
    btn_eletrica = ft.ElevatedButton(text="Elétrica", on_click=lambda e: mostrar_eletrica(page), width=200)
    page.add(btn_eletrica)
    page.add(btn_parede)
    
    page.update()