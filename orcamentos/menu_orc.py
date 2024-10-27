import flet as ft
from exemplos import exemplo
from orcamentos import orc_eletrica, orc_paredes, orc_laje, orc_contrapiso, orc_telhado


def orcamento(page):
    page.controls.clear()
    page.add(ft.Text("Tela de Orçamento", size=24))
    
    btn_parede = ft.ElevatedButton(text="Parede", on_click=lambda e:            orc_paredes.mostrar_parede(page), width=200,)
    btn_eletrica = ft.ElevatedButton(text="Elétrica", on_click=lambda e:        orc_eletrica.mostrar_eletrica(page), width=200)
    btn_laje = ft.ElevatedButton(text="Laje", on_click=lambda e:                orc_laje.mostrar_laje(page), width=200)
    btn_contrapiso = ft.ElevatedButton(text="Contrapiso", on_click=lambda e:    orc_contrapiso.mostrar_contrapiso(page), width=200)
    btn_telhado = ft.ElevatedButton(text="Telhado", on_click=lambda e:          orc_telhado.mostrar_telhado(page), width=200)
    btn_exemplo = ft.ElevatedButton(text="Exemplo", on_click=lambda e:          exemplo(page), width=200)

    page.add(
        btn_exemplo, btn_eletrica, 
        btn_parede, btn_laje, 
        btn_contrapiso, btn_telhado
    )

    page.update()
