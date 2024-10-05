import flet as ft
import styles as stl

def exemplo(page: ft.Page):
    page.controls.clear()
    
    # Container com sombra
    shadow_container = ft.Container(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.FAVORITE, color="pink"),
                ft.Icon(name=ft.icons.AUDIOTRACK, color="green"),
                ft.Icon(name=ft.icons.BEACH_ACCESS, color="blue"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        ),
        **stl.container_style,
    )
    voltar_btn = ft.ElevatedButton(text="Voltar", on_click=lambda e: voltar(page),**stl.button_style_voltar)
    page.add(shadow_container, voltar_btn)
    page.update()
# Exemplo de execução
#ft.app(target=exemplo)
def voltar(page):
    page.controls.clear()    
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento