import flet as ft
import user

import custom.styles as stl
from models.db import cadastrar_usuario


def mostrar_cadastro(page):
    page.controls.clear()
    page.add(
        ft.Text(
            "Tela de Cadastro", size=24, color=ft.colors.BLUE, weight=ft.FontWeight.BOLD
        )
    )

    nome_input = ft.TextField(label="Nome", **stl.input_style)
    email_input = ft.TextField(label="E-mail", **stl.input_style)
    senha_input = ft.TextField(label="Senha", password=True, **stl.input_style)

    cadastrar_button = ft.ElevatedButton(
        text="Cadastrar",
        on_click=lambda e: processar_cadastro(
            page, nome_input.value, email_input.value, senha_input.value
        ),
        width=300,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=5,
        ),
    )
    voltar_login_button = ft.ElevatedButton(
        text="Voltar ao Login", on_click=lambda e: user.login.mostrar_login(page), on_hover= stl.hover_effect_voltar
    )

    page.add(
        nome_input, email_input, senha_input, cadastrar_button, voltar_login_button
    )
    page.update()


def processar_cadastro(page, nome, email, senha):
    if not nome or not email or not senha:
        print("Todos os campos são obrigatórios!")
        page.add(ft.Text("Todos os campos são obrigatórios!", color=ft.colors.RED))
    else:
        try:
            cadastrar_usuario(nome, email, senha)
            print(f"Usuário {nome} cadastrado com sucesso!")
            page.add(
                ft.Text(
                    f"Usuário {nome} cadastrado com sucesso!", color=ft.colors.GREEN
                )
            )
            user.login.mostrar_login(page)  # Redireciona para a tela de login
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            page.add(
                ft.Text(f"Erro ao cadastrar usuário: {str(e)}", color=ft.colors.RED)
            )

    page.update()
