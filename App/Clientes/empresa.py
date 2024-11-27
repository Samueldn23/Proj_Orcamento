import flet as ft 
from custom.styles_utils import get_style_manager
from custom.button import Voltar
gsm= get_style_manager()

def tela_empresa(page: ft.Page):
    page.controls.clear()
    page.add(
        gsm.create_button(
            text="Voltar",
            on_click=lambda _: Voltar.principal(page),
            icon=ft.icons.ARROW_BACK,
        )
    )