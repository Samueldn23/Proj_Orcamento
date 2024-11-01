import flet as ft
import custom.styles as stl
from App.orcamentos import menu_orc
from examples.exemplos import exemplo


def mostrar_menu(page):
    page.controls.clear()
    page.add(ft.Text("Tela Inicial", size=24))

    btn_Orcamento = ft.ElevatedButton(
        text="Orcamentos",
        on_click=lambda e: menu_orc.orcamento(page),
        width=200,
        on_hover=stl.hover_effect_prinicipal,
    )

    btn_exemplo = ft.ElevatedButton(
        text="Exemplo",
        on_click=lambda e: exemplo(page),
        width=200,
        on_hover=stl.hover_effect_prinicipal,
    )

    page.add(btn_exemplo, btn_Orcamento)
    page.update()
