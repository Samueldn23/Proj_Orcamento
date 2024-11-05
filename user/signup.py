import flet as ft
from typing import Optional
import user
import custom.styles as stl
from models.db import cadastrar_usuario
import time

class SignupPage:
    """Classe para gerenciar a página de cadastro"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.error_text: Optional[ft.Text] = None
        self.success_text: Optional[ft.Text] = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página"""
        self.nome_input = ft.TextField(
            label="Nome",
            prefix_icon=ft.icons.PERSON,
            helper_text="Digite seu nome completo",
            **stl.input_style,
        )

        self.email_input = ft.TextField(
            label="E-mail",
            prefix_icon=ft.icons.EMAIL,
            helper_text="Digite um e-mail válido",
            **stl.input_style,
        )

        self.senha_input = ft.TextField(
            label="Senha",
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            helper_text="Mínimo 6 caracteres",
            **stl.input_style,
        )

        self.error_text = ft.Text(
            color=ft.colors.RED_600,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )

        self.success_text = ft.Text(
            color=ft.colors.GREEN_600,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )

    def _create_buttons(self):
        """Cria os botões da página"""
        return [
            ft.ElevatedButton(
                text="Cadastrar",
                icon=ft.icons.PERSON_ADD,
                on_click=self._handle_signup,
                width=300,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    elevation=5,
                ),
            ),
            ft.ElevatedButton(
                text="Voltar ao Login",
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: user.login.mostrar_login(self.page),
                on_hover=stl.hover_effect_voltar,
            ),
        ]

    def _validate_inputs(self) -> tuple[bool, str]:
        """Valida os inputs do formulário"""
        if not all(
            [self.nome_input.value, self.email_input.value, self.senha_input.value]
        ):
            return False, "Todos os campos são obrigatórios!"

        if len(self.senha_input.value) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres!"

        if "@" not in self.email_input.value:
            return False, "E-mail inválido!"

        return True, ""

    def _show_message(self, message: str, is_error: bool = True):
        """Exibe mensagem de erro ou sucesso"""
        if is_error:
            self.error_text.value = message
            self.error_text.visible = True
            self.success_text.visible = False
        else:
            self.success_text.value = message
            self.success_text.visible = True
            self.error_text.visible = False
        self.page.update()

    def _handle_signup(self, _):
        """Processa o cadastro do usuário"""
        valid, message = self._validate_inputs()
        if not valid:
            self._show_message(message)
            return

        try:
            cadastrar_usuario(
                self.nome_input.value, self.email_input.value, self.senha_input.value
            )
            self._show_message(
                f"Usuário {self.nome_input.value} cadastrado com sucesso!", False
            )
            time.sleep(2)
            # Redireciona após 2 segundos
            #self.page.window.destroy()
            user.login.mostrar_login(self.page)
        except Exception as e:
            self._show_message(f"Erro ao cadastrar usuário: {str(e)}")

    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cadastro de Usuário",
                        size=24,
                        color=ft.colors.BLUE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.nome_input,
                    self.email_input,
                    self.senha_input,
                    self.error_text,
                    self.success_text,
                    *self._create_buttons(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=40,
            alignment=ft.alignment.center,
        )


def mostrar_cadastro(page: ft.Page):
    """Função helper para mostrar a página de cadastro"""
    page.controls.clear()
    signup_page = SignupPage(page)
    page.add(signup_page.build())
    page.update()
