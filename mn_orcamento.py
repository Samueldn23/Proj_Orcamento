import flet as ft
from orc_paredes import mostrar_parede  # Importa a função mostrar_parede
from orc_eletrica import mostrar_eletrica  # Importa a função mostrar_eletrica
from orc_laje import mostrar_laje
from orc_contrapiso import mostrar_contrapiso 

def orcamento(page):
    page.controls.clear()
    page.add(ft.Text("Tela de Orçamento", size=24))

    btn_parede = ft.ElevatedButton(text="Parede", on_click=lambda e: mostrar_parede(page), width=200)
    btn_eletrica = ft.ElevatedButton(text="Elétrica", on_click=lambda e: mostrar_eletrica(page), width=200)
    btn_laje = ft.ElevatedButton(text="Laje", on_click=lambda e: mostrar_laje(page), width=200)
    btn_contrapiso = ft.ElevatedButton(text="Contrapiso", on_click=lambda e: mostrar_contrapiso(page), width=200)
    
    page.add(
        btn_eletrica,
        btn_parede,
        btn_laje,
        btn_contrapiso)
    
    
    page.update()