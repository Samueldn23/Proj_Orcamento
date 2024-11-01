import flet as ft
import App.orcamentos as orc
import custom.styles as stl
import custom.button as btn


def orcamento(page):
    page.controls.clear()
    page.add(ft.Text("Tela de Orçamento", size=24))

    # Definindo o botão com o efeito de hover
    btn_parede = ft.ElevatedButton(
        text="Parede",
        on_click=lambda e: orc.paredes.mostrar_parede(page),
        width=200,
        on_hover=stl.hover_effect,
    )
    btn_eletrica = ft.ElevatedButton(
        text="Elétrica",
        on_click=lambda e: orc.eletrica.mostrar_eletrica(page),
        width=200,
        on_hover=stl.hover_effect,
    )
    btn_laje = ft.ElevatedButton(
        text="Laje",
        on_click=lambda e: orc.laje.mostrar_laje(page),
        width=200,
        on_hover=stl.hover_effect,
    )
    btn_contrapiso = ft.ElevatedButton(
        text="Contrapiso",
        on_click=lambda e: orc.contrapiso.mostrar_contrapiso(page),
        width=200,
        on_hover=stl.hover_effect,
    )
    btn_telhado = ft.ElevatedButton(
        text="Telhado",
        on_click=lambda e: orc.telhado.mostrar_telhado(page),
        width=200,
        on_hover=stl.hover_effect,
    )
    

    voltar_btn = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda e: btn.voltar.principal(page),
        on_hover=stl.hover_effect_voltar,
    )

    page.add(
        btn_eletrica, btn_parede, btn_laje, btn_contrapiso, btn_telhado, voltar_btn
    )

    page.update()
