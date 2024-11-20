import flet as ft
import custom.button as clk
from custom.styles_utils import get_style_manager

gsm = get_style_manager()

def main(page: ft.Page):
    # Definir os temas e estilos da aplicação
    page.controls.clear()
    page.title = "Aplicativo de Orçamento para Construção"
    
    
    btn_voltar = ft.ElevatedButton(
        text="Voltar",
        on_click=lambda e: clk.voltar.principal(page),
    )
    btn_voltar.on_hover = gsm.create_button_hover_effect(
        button=btn_voltar,
        text_color=ft.colors.WHITE,
        hover_color=ft.colors.AMBER
    )

    page.add(
        btn_voltar,
        ft.Divider(),  

        get_style_manager().create_button_custom(
            text="teste 3",
            on_click=lambda _: print("teste 3"),
            icon="icons/eletrica.png",
        ),
        gsm.create_button_custom(
            text="teste 4",
            on_click=lambda _: print("teste 4"),
            icon="icons/eletrica.png",
            width=150,
            icon_color=ft.colors.BLUE,
            hover_icon_color=ft.colors.WHITE,
            hover_color=ft.colors.AMBER,
        ),
        
    )

# ft.app(target=main)
