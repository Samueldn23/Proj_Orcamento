import flet as ft
import styles as stl
from mn_orcamento import orcamento


def main(page: ft.Page):
    page.adaptive = True
    page.title = "Aplicativo de Orçamento"
    
    stl.aplicar_tema(page)
    mostrar_login(page)

# Variável global para armazenar a mensagem de erro
error_message = None

def mostrar_login(page):
    global error_message
    page.controls.clear()
    page.add(ft.Text("Tela de Login", size=24, color=ft.colors.BLUE, weight=ft.FontWeight.BOLD))

    username_input = ft.TextField(label="Usuário", **stl.input_style)
    password_input = ft.TextField(label="Senha", password=True, **stl.input_style)

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