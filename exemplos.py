import flet as ft

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
            #alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=ft.colors.CYAN,
        padding=ft.padding.all(16),
        border_radius=ft.border_radius.all(8),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
    )
    
    page.add(shadow_container)
    page.update()
# Exemplo de execução
#ft.app(target=exemplo)
def voltar(page):
    page.controls.clear()    
    from mn_orcamento import orcamento  # Importa a função orcamento
    orcamento(page)  # Retorna à tela de Orçamento