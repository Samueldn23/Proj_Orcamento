"""modulo da tela da empresa"""

import time
from typing import Optional

import flet as ft

from App.orcamentos import menu_orc
from custom.button import Voltar
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


class cadastro:
    """cadastro da empresa"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.scroll = "adaptive"
        self.error_text: Optional[ft.text] = None
        self.success_text: Optional[ft.text] = None
        self._init_controls()

    def _init_controls(self):
        self.razao_social_input = ft.TextField(
            label="Razão Social",
            prefix_icon=ft.Icons.PERSON,
            helper_text="Digite Sua Razão social",
            keyboard_type=ft.KeyboardType.NAME,
            **gsm.input_style,
        )

        self.nome_input = ft.TextField(
            label="Nome Da Empresa",
            prefix_icon=ft.Icons.CORPORATE_FARE,
            helper_text="Digite o Nome Da Empresa",
            keyboard_type=ft.KeyboardType.NAME,
            **gsm.input_style,
        )

        self.cnpj_input = ft.TextField(
            label="CNPJ",
            prefix_icon=ft.Icons.PERSON,
            helper_text="Digite seu CNPJ",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )
        self.telefone_input = ft.TextField(
            label="Telefone",
            prefix_icon=ft.Icons.PHONE,
            helper_text="Digite o telefone da Empresa",
            keyboard_type=ft.KeyboardType.PHONE,
            **gsm.input_style,
        )
        self.email_input = ft.TextField(
            label="E-mail",
            prefix_icon=ft.Icons.EMAIL,
            helper_text="Digite um e-mail válido",
            keyboard_type=ft.KeyboardType.EMAIL,
            **gsm.input_style,
        )
        self.cep_input = ft.TextField(
            label="CEP",
            prefix_icon=ft.Icons.LOCATION_ON,
            helper_text="Digite seu CEP",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.endereco_input = ft.TextField(
            label="Endereço",
            prefix_icon=ft.Icons.LOCATION_ON,
            helper_text="Digite seu endereço",
            keyboard_type=ft.KeyboardType.TEXT,
            **gsm.input_style,
        )
        self.numero_input = ft.TextField(
            label="Número",
            prefix_icon=ft.Icons.LOCATION_ON,
            helper_text="Digite o número do endereço",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.bairro_input = ft.TextField(
            label="Bairro",
            prefix_icon=ft.Icons.LOCATION_ON,
            helper_text="Digite o bairro",
            keyboard_type=ft.KeyboardType.TEXT,
            **gsm.input_style,
        )

        self.cidade_input = ft.TextField(
            label="Cidade",
            prefix_icon=ft.Icons.LOCATION_ON,
            helper_text="Digite a cidade",
            keyboard_type=ft.KeyboardType.TEXT,
            **gsm.input_style,
        )

        self.estado_input = ft.TextField(
            label="Estado",
            prefix_icon=ft.Icons.LOCATION_ON,
            helper_text="Digite o estado",
            keyboard_type=ft.KeyboardType.TEXT,
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
        """criar os botões da página"""
        return [
            gsm.create_button(
                text="salvar",
                icon=ft.Icons.SAVE,
                on_click=self._salvar_empresa,
                hover_color=None,
                hover_color_button=ft.Colors.GREEN,
            ),
            gsm.create_button(
                text="Voltar",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: Voltar.principal(self.page),
                hover_color=gsm.colors.VOLTAR,
            ),
        ]

    def _validar_campos(self) -> tuple[bool, str]:
        """Valida os campos do formulário"""
        if not self.nome_input.value:
            self._message("O campo nome é obrigatório", True)
            return False

        if not self.telefone_input.value:
            self._message("O campo telefone é obrigatório", True)
            return False

        return (True,)

    def _message(self, message: str, is_error: bool = True):
        """exibe uma mensagem na tela"""
        if is_error:
            self.error_text.value = message
            self.error_text.visible = True
            self.success_text.visible = False
        else:
            self.success_text.value = message
            self.success_text.visible = True
            self.error_text.viseble = False
            self.page.update()

    def _salvar_empresa(self, _):
        """salvar a empresa no banco de dados"""
        validar, message = self._validar_campos()
        if not validar:
            self._message(message, True)
            return

        try:
            self._message(
                f"Cliente {self.nome_input.value} cadastrado com sucesso!", False
            )
            time.sleep(2)
            menu_orc.mostrar_orcamento(self.page)
        except ValueError as ve:  # Exceção específica para problemas com os dados
            print(ve)
            self._message("Erro ao cadastrar cliente: dados inválidos.", True)
        except TypeError as te:  # Exceção específica se houver um erro de tipo
            print(te)
            self._message("Erro ao cadastrar cliente: tipo de dado inválido.", True)

    def build(self):
        """Cria o formulário da página"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cadastro da Empresa", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.Colors.BLUE_GREY_100),
                    ft.Container(
                        content=ft.Column(
                            [
                                self.razao_social_input,
                                self.nome_input,
                                self.cnpj_input,
                                self.email_input,
                                self.telefone_input,
                                self.endereco_input,
                                self.numero_input,
                                self.bairro_input,
                                self.cidade_input,
                                self.estado_input,
                                self.cep_input,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        **gsm.container_style,
                    ),
                    ft.Divider(height=20, color=ft.Colors.BLUE_GREY_100),
                    self.error_text,
                    self.success_text,
                    *self._create_buttons(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=600,
            )
        )


def tela_cadastro_empresa(page: ft.Page):
    """Tela de cadastro de clientes"""
    page.controls.clear()
    tela_cadastro_empresa_page = cadastro(page)
    page.add(tela_cadastro_empresa_page.build())

    page.update()
