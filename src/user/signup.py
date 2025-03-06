"""Menu de cadastro de usuário. user/signup.py"""

import time

import flet as ft

from src.custom.styles_utils import get_style_manager
from src.user import cadastrar_usuario, login

gsm = get_style_manager()


class SignupPage:
    """Classe para gerenciar a página de cadastro"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.error_text: ft.Text | None = None
        self.success_text: ft.Text | None = None
        self._init_controls()

    def _init_controls(self):
        """Inicializa os controles da página"""
        self.nome_input = ft.TextField(
            label="Nome",
            prefix_icon=ft.Icons.PERSON,
            helper_text="Digite seu nome completo",
            keyboard_type=ft.KeyboardType.NAME,
            **gsm.input_style,
        )

        self.email_input = ft.TextField(
            label="E-mail",
            prefix_icon=ft.Icons.EMAIL,
            helper_text="Digite um e-mail válido",
            keyboard_type=ft.KeyboardType.EMAIL,
            **gsm.input_style,
        )

        self.senha_input = ft.TextField(
            label="Senha",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            helper_text="Mínimo 6 caracteres",
            **gsm.input_style,
        )

        self.senha_check_input = ft.TextField(
            label="Confirma Senha",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            helper_text="As senhas devem coincidir",
            **gsm.input_style,
        )

        self.error_text = ft.Text(
            color=ft.Colors.RED_600,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )

        self.success_text = ft.Text(
            color=ft.Colors.GREEN_600,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )

    def _create_buttons(self):
        """Cria os botões da página"""
        return [
            ft.ElevatedButton(
                text="Cadastrar",
                icon=ft.Icons.PERSON_ADD,
                on_click=self._handle_signup,
                width=300,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE,
                icon_color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    elevation=5,
                ),
            ),
            gsm.create_button(
                text="Voltar ao Menu Principal",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: login.mostrar_tela(self.page),
                hover_color=gsm.colors.VOLTAR,
                width=300,
            ),
        ]

    def _validate_inputs(self) -> tuple[bool, str]:
        """Valida os inputs do formulário"""
        if "@" not in self.email_input.value:
            return False, "E-mail inválido!"

        if len(self.senha_input.value) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres!"

        if self.senha_input.value != self.senha_check_input.value:
            return False, "As senhas não coincidem!"

        if not self.nome_input.value.strip():
            return False, "O nome é obrigatório!"

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
            if cadastrar_usuario(self.nome_input.value, self.email_input.value, self.senha_input.value):
                self._show_message(f"Usuário {self.nome_input.value} cadastrado com sucesso!", False)
                time.sleep(2)
                login.mostrar_tela(self.page)
            else:
                self._show_message("Erro ao cadastrar usuário. Tente novamente!")
        except Exception as e:  # pylint: disable=broad-exception-caught
            self._show_message(f"Erro inesperado: {e!s}")

    def build(self):
        """Constrói a interface da página"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cadastro de Usuário",
                        size=24,
                        color=ft.Colors.BLUE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.nome_input,
                    self.email_input,
                    self.senha_input,
                    self.senha_check_input,
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


def tela_cadastro(page: ft.Page):
    """Função helper para mostrar a página de cadastro"""
    page.controls.clear()
    signup_page = SignupPage(page)
    page.add(signup_page.build())
    page.update()
