import flet as ft
from mn_orcamento import orcamento

def main(page: ft.Page):
    page.title = "Aplicativo de Orçamento"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    mostrar_login(page)

# Variável global para armazenar a mensagem de erro
error_message = None

def mostrar_login(page):
    global error_message
    page.controls.clear()
    page.add(ft.Text("Tela de Login", size=24))

    username_input = ft.TextField(label="Usuário",width=200)
    password_input = ft.TextField(label="Senha", password=True,width=200)

    login_button = ft.ElevatedButton(text="Login", on_click=lambda e: fazer_login(page, username_input.value, password_input.value))
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