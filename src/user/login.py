"""Módulo de login"""

import os

import flet as ft
from dotenv import load_dotenv

from custom.styles_utils import get_style_manager
from src.navigation.router import navigate_to_menu
from src.infrastructure.database.repositories import UserRepository

from .signup import tela_cadastro

gsm = get_style_manager()
user_repo = UserRepository()
load_dotenv()


class LoginPage:
    """Classe para representar a página de login"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.error_message = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página de login"""
        self.email_input = ft.TextField(
            label="Email",
            autofocus=True,
            value=os.getenv("USER_NAME", ""),  # Valor padrão vazio se não existir
            **gsm.input_style,
        )

        self.password_input = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            value=os.getenv("USER_PASS", ""),  # Valor padrão vazio se não existir
            **gsm.input_style,
        )

        self.login_button = ft.ElevatedButton(
            text="Entrar",
            width=300,
            on_click=self.fazer_login,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
            ),
        )

        self.signup_button = ft.TextButton(
            text="Não tem uma conta? Cadastre-se",
            on_click=lambda _: tela_cadastro(self.page),
        )

        self.error_text = ft.Text(color=ft.Colors.RED, visible=False)

    def mostrar_erro(self, mensagem: str):
        """Exibe uma mensagem de erro na tela"""
        self.error_text.value = mensagem
        self.error_text.visible = True
        self.page.update()

    async def fazer_login(self, _):
        """Processa a tentativa de login"""
        if not self.email_input.value or not self.password_input.value:
            self.mostrar_erro("Preencha todos os campos!")
            return

        self.page.show_loading = True
        self.error_text.visible = False
        self.page.update()

        try:
            if user_repo.login_with_password(
                self.email_input.value, self.password_input.value
            ):
                self.page.open(
                    ft.SnackBar(
                        content=ft.Text(
                            value="Login realizado com sucesso!",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor=ft.Colors.GREEN,
                    ),
                )
                navigate_to_menu(self.page)
            else:
                self.mostrar_erro("Usuário ou senha inválidos")
        except ValueError as e:
            self.mostrar_erro(f"Erro ao fazer login: {str(e)}")
            print(f"Erro ao fazer login: {str(e)}")
        finally:
            self.page.show_loading = True
            self.page.update()

    def build(self):
        """Constrói a interface da página de login"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Bem-vindo", size=32, weight=ft.FontWeight.BOLD),
                    self.email_input,
                    self.password_input,
                    self.login_button,
                    self.error_text,
                    ft.Divider(height=20),
                    self.signup_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=40,
            alignment=ft.alignment.center,
        )


def mostrar_tela(page: ft.Page):
    """Mostra a tela de login"""

    def handle_login_success(_):
        navigate_to_menu(page)

    page.controls.clear()
    login_page = LoginPage(page)
    page.add(login_page.build())
    page.update()
