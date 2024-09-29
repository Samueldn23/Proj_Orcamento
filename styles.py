import flet as ft

def aplicar_tema(page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400  # Largura da janela
    page.window_height = 600  # Altura da janela
    
    page.window.bgcolor = ft.colors.TRANSPARENT
    page.bgcolor = ft.colors.TRANSPARENT
    page.window.title_bar_hidden = False #Se a barra de título da janela do aplicativo deve ser ocultada.
    page.window.frameless = False #Se a janela do aplicativo deve ser sem quadros.

    page.window.opacity = 1.0 #Define a opacidade de uma janela nativa do sistema operacional.

    page.window.center()

    # Definindo um tema
    page.theme = ft.Theme(
        primary_color=ft.colors.BLUE,
        font_family="Arial",
    )

input_style = {
    "keyboard_type": ft.KeyboardType.NUMBER,
    "width": 300,
    "bgcolor": ft.colors.with_opacity(0.8, ft.colors.GREY_900),
}

button_style = {
    "width": 200,
    "color": ft.colors.WHITE,
    "bgcolor": ft.colors.BLUE,
}
button_style_voltar = {
    "width": 200,
    "color": ft.colors.WHITE,
    "bgcolor": ft.colors.RED,
}