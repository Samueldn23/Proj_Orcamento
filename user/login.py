import os
import flet as ft
from dotenv import load_dotenv
import menu
from models.db import autenticar_usuario
from .signup import mostrar_cadastro
from custom.styles_utils import get_style_manager

gsm = get_style_manager()
load_dotenv()


class LoginPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.error_message = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página de login"""
        self.username_input = ft.TextField(
            label="Email",
            autofocus=True,
            value=os.getenv("USERNAME2", ""),  # Valor padrão vazio se não existir
            **gsm.input_style,
        )

        self.password_input = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            value=os.getenv("PASSWORD", ""),  # Valor padrão vazio se não existir
            **gsm.input_style,
        )

        self.login_button = ft.ElevatedButton(
            text="Entrar",
            width=300,
            on_click=self.fazer_login,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
            ),
        )

        self.signup_button = ft.TextButton(
            text="Não tem uma conta? Cadastre-se",
            on_click=lambda _: mostrar_cadastro(self.page),
        )

        self.error_text = ft.Text(color=ft.colors.RED, visible=False)

    def mostrar_erro(self, mensagem: str):
        """Exibe uma mensagem de erro na tela"""
        self.error_text.value = mensagem
        self.error_text.visible = True
        self.page.update()

    async def fazer_login(self, _):
        """Processa a tentativa de login"""
        if not self.username_input.value or not self.password_input.value:
            self.mostrar_erro("Preencha todos os campos!")
            return

        self.page.show_loading = True
        self.error_text.visible = False
        self.page.update()

        try:
            if autenticar_usuario(self.username_input.value, self.password_input.value):
                self.page.open(
                    ft.SnackBar(
                        content=ft.Text("Login realizado com sucesso!"),
                        bgcolor=ft.colors.GREEN,
                    ),
                )
                menu.mostrar_menu(self.page)
            else:
                self.mostrar_erro("Usuário ou senha inválidos")
        except Exception as e:
            self.mostrar_erro(f"Erro ao fazer login: {str(e)}")
            print(f"Erro ao fazer login: {str(e)}")
        finally:
            self.page.show_loading = False
            self.page.update()

    def build(self):
        """Constrói a interface da página de login"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Bem-vindo", size=32, weight=ft.FontWeight.BOLD),
                    self.username_input,
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


def mostrar_login(page: ft.Page):
    """Função helper para mostrar a página de login"""
    page.controls.clear()
    login_page = LoginPage(page)
    page.add(login_page.build())
    page.update()
