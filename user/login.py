import os

import flet as ft
from dotenv import load_dotenv

import custom.styles as stl
from models.db import autenticar_usuario

from . import signup  # Importa a função de cadastro

load_dotenv()

# Variável global para armazenar a mensagem de erro
error_message = None


def mostrar_login(page):
    global error_message
    page.controls.clear()
    page.add(
        ft.Text(
            "Tela de Login", size=24, color=ft.colors.BLUE, weight=ft.FontWeight.BOLD
        )
    )

    username_input = ft.TextField(label="Email", **stl.input_style)
    password_input = ft.TextField(label="Senha", password=True, **stl.input_style)

    username_input.value = os.getenv("USERNAME2")
    password_input.value = os.getenv("PASSWORD")

    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda e: fazer_login(
            page, username_input.value, password_input.value
        ),
        width=300,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=5,
        ),
    )

    cadastrar_button = ft.TextButton(
        text="Não tem uma conta? Cadastre-se",
        on_click=lambda e: signup.mostrar_cadastro(page),
    )

    page.update()
    page.add(username_input, password_input, login_button, cadastrar_button)

    # Adiciona a mensagem de erro, se existir
    if error_message:
        page.add(ft.Text(error_message, color=ft.colors.RED))

    page.update()


def fazer_login(page, username, password):
    import menu  # Importa a função de autenticação

    global error_message

    # Limpa a mensagem de erro anterior
    error_message = None

    # Verifica se o usuário e a senha estão corretos
    if autenticar_usuario(username, password):
        menu.mostrar_menu(
            page
        )  # Se o login for bem-sucedido, navega para a tela de orçamento
    else:
        error_message = "Usuário ou senha incorretos!"  # Atualiza a mensagem de erro
        mostrar_login(page)  # Atualiza a tela de login para mostrar a nova mensagem
