import flet as ft

def aplicar_tema(page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    #page.window_width = 400  # Largura da janela
    #page.window_height = 600  # Altura da janela
    
    # Definindo um tema
    page.theme = ft.Theme(
        primary_color=ft.colors.BLUE,
        font_family="Arial",
    )