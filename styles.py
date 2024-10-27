import flet as ft

def aplicar_tema(page):
    # Centraliza o conteúdo verticalmente na página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # Centraliza o conteúdo horizontalmente na página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Define a largura da janela do aplicativo
    page.window.width = 400 
    # Define a altura da janela do aplicativo
    page.window.height = 800  
    
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

    # Adiciona o estilo de fundo moderno e escuro
    page.bgcolor = ft.colors.with_opacity(0.1, ft.colors.BLACK)                 # Fundo escuro
    page.gradient = ft.LinearGradient(                                          # Gradiente linear
        colors=[ft.colors.BLACK, ft.colors.BLUE_GREY_800],                      # Cores do gradiente
        begin=ft.alignment.top_center,                                          # Início do gradiente (canto superior esquerdo)
        end=ft.alignment.bottom_center,                                         # Fim do gradiente (canto inferior direito)
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
    "bgcolor": ft.colors.with_opacity(0.9, ft.colors.GREY_900),  # Cor de fundo com opacidade leve
    "margin": 15,                                           # Margem ao redor do contêiner
    "padding": 20,                                          # Preenchimento interno do contêiner
    "alignment": ft.alignment.center,                       # Alinhamento do conteúdo do contêiner
    "width": 350,                                          # Largura do contêiner
    "border_radius": 15,                                   # Raio da borda para cantos arredondados
    "shadow": ft.BoxShadow(                                 # Estilo de sombra do contêiner
        spread_radius=2,                                   # Raio de expansão da sombra
        blur_radius=20,                                    # Raio de desfoque da sombra
        color=ft.colors.with_opacity(0.2, ft.colors.WHITE),  # Cor da sombra com opacidade 
        offset=ft.Offset(0, 4),                            # Deslocamento da sombra para baixo
        blur_style=ft.ShadowBlurStyle.NORMAL,             # Estilo de desfoque da sombra
    )
}