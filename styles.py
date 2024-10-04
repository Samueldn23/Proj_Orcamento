import flet as ft

def aplicar_tema(page):
    # Centraliza o conteúdo verticalmente na página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # Centraliza o conteúdo horizontalmente na página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Define a largura da janela do aplicativo
    page.window_width = 400  
    # Define a altura da janela do aplicativo
    page.window_height = 600  
    
    # Define se a barra de título da janela deve ser oculta
    page.window.title_bar_hidden = False 
    # Define se a janela do aplicativo deve ser sem quadros
    page.window.frameless = False 

    # Define a opacidade da janela (1.0 é totalmente opaco)
    page.window.opacity = 1.0 

    # Centraliza a janela na tela
    page.window.center()

    # Definindo um tema para o aplicativo
    page.theme = ft.Theme(
        primary_color=ft.colors.BLUE,  # Cor primária do tema
        font_family="Arial",            # Fonte utilizada no tema
    )

# Estilo para campos de entrada
input_style = {
    "keyboard_type": ft.KeyboardType.NUMBER,  # Define o tipo de teclado como numérico
    "width": 300,                             # Largura do campo de entrada
    "bgcolor": ft.colors.with_opacity(0.8, ft.colors.GREY_900),  # Cor de fundo com opacidade
    "border_radius": 10,                      # Raio da borda para cantos arredondados
}

# Estilo para botões gerais
button_style = {
    "width": 200,                             # Largura do botão
    "color": ft.colors.WHITE,                 # Cor do texto do botão
    "bgcolor": ft.colors.BLUE,                # Cor de fundo do botão
}

# Estilo para o botão "Voltar"
button_style_voltar = {
    "width": 200,                             # Largura do botão
    "color": ft.colors.WHITE,                 # Cor do texto do botão
    "bgcolor": ft.colors.RED,                 # Cor de fundo do botão
}

# Estilo para contêineres
container_style = {
    "bgcolor": ft.colors.with_opacity(0.8, ft.colors.GREY_900),  # Cor de fundo com opacidade
    "margin": 10,                             # Margem ao redor do contêiner
    "padding": 10,                            # Preenchimento interno do contêiner
    "alignment": ft.alignment.center,         # Alinhamento do conteúdo do contêiner
    "width": 300,                             # Largura do contêiner
    "border_radius": 10,                      # Raio da borda para cantos arredondados
    "shadow": ft.BoxShadow(                   # Estilo de sombra do contêiner
        spread_radius=1,                      # Raio de expansão da sombra
        blur_radius=15,                       # Raio de desfoque da sombra
        color=ft.colors.BLUE_GREY_400,        # Cor da sombra
        offset=ft.Offset(0, 0),               # Deslocamento da sombra
        blur_style=ft.ShadowBlurStyle.INNER,  # Estilo de desfoque da sombra
    )
}