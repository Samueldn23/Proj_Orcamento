import flet as ft
from mn_orcamento import orcamento

def main(page: ft.Page):
    page.title = "Aplicativo de Orçamento"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400  # Largura da janela
    page.window_height = 600  # Altura da janela

    # Definindo um tema
    page.theme = ft.Theme(
        primary_color=ft.colors.BLUE,
        #accent_color=ft.colors.LIGHT_BLUE,
        font_family="Arial",
    )

    mostrar_login(page)

# Variável global para armazenar a mensagem de erro
error_message = None

def mostrar_login(page):
    global error_message
    page.controls.clear()
    page.bgcolor = ft.colors.SHADOW # Definindo a cor de fundo
    page.add(ft.Text("Tela de Login", size=24, color=ft.colors.BLUE, weight=ft.FontWeight.BOLD))

    # Tela de login com estilo CSS
    #page.add(ft.Text("Tela de Login", size=24, style="font-weight: bold; color: blue;"))

    username_input = ft.TextField(label="Usuário", width=300, bgcolor=ft.colors.GREY_900)
    password_input = ft.TextField(label="Senha", password=True, width=300, bgcolor=ft.colors.GREY_900)

    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda e: fazer_login(page, username_input.value, password_input.value),
        width=300,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=5,
        )
    )
    page.add(username_input, password_input, login_button)

    # Adiciona a mensagem de erro, se existir
    if error_message:
        page.add(ft.Text(error_message, color=ft.colors.RED))

    page.update()

def fazer_login(page, username, password):
    global error_message

    # Limpa a mensagem de erro anterior
    error_message = None

    # Aqui você pode adicionar lógica de autenticação
    if username == "" and password == "":  # Exemplo de autenticação
        orcamento(page)  # Se o login for bem-sucedido, vai para a tela de orçamento
    else:
        error_message = "Usuário ou senha incorretos!"  # Atualiza a mensagem de erro
        mostrar_login(page)  # Atualiza a tela de login para mostrar a nova mensagem

# Iniciando o aplicativo
ft.app(target=main)