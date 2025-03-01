"""Modulo de cadastro de clientes. cadastro.py"""

import time

import flet as ft

from src.core.orcamento import menu_orc
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import ClientRepository, UserRepository

gsm = get_style_manager()
Cliente = ClientRepository()
Usuario = UserRepository()


class Cadastro:
    """Cadastro de clientes"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.error_text: ft.Text | None = None
        self.success_text: ft.Text | None = None
        self._init_controls()

    def _init_controls(self):
        self.nome_input = ft.TextField(
            label="Nome",
            prefix_icon=ft.Icons.PERSON,
            helper_text="Digite seu nome completo",
            keyboard_type=ft.KeyboardType.NAME,
            **gsm.input_style,
        )

        self.cpf_input = ft.TextField(
            label="CPF",
            prefix_icon=ft.Icons.PERSON,
            helper_text="Digite seu CPF",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.data_nascimento_input = ft.TextField(
            label="Data de Nascimento",
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            helper_text="Digite sua data de nascimento",
            keyboard_type=ft.KeyboardType.DATETIME,
            **gsm.input_style,
        )

        self.rg_input = ft.TextField(
            label="RG",
            prefix_icon=ft.Icons.PERSON,
            helper_text="Digite seu RG",
            keyboard_type=ft.KeyboardType.NUMBER,
            **gsm.input_style,
        )

        self.email_input = ft.TextField(
            label="E-mail",
            prefix_icon=ft.Icons.EMAIL,
            helper_text="Digite um e-mail válido",
            keyboard_type=ft.KeyboardType.EMAIL,
            **gsm.input_style,
        )

        self.telefone_input = ft.TextField(
            label="Telefone",
            prefix_icon=ft.Icons.PHONE,
            helper_text="Digite seu telefone",
            keyboard_type=ft.KeyboardType.PHONE,
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
        """Cria os botões da página"""
        from src.core.cliente import clientes

        return [
            gsm.create_button(
                text="Salvar",
                icon=ft.Icons.SAVE,
                on_click=self._salvar_cliente,
                hover_color=None,
                hover_color_button=ft.Colors.GREEN,
                width=130,
            ),
            gsm.create_button(
                text="Voltar",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: clientes.tela_clientes(self.page),
                hover_color=gsm.colors.VOLTAR,
                width=130,
            ),
        ]

    def _validar_campos(self) -> tuple[bool, str]:
        """Valida os campos do formulário"""
        if not self.nome_input.value:
            self._message("O campo nome é obrigatório", True)
            return False, "O campo nome é obrigatório"  # Adiciona a mensagem de erro

        if not self.telefone_input.value:
            self._message("O campo telefone é obrigatório", True)
            return (
                False,
                "O campo telefone é obrigatório",
            )  # Adiciona a mensagem de erro

        return True, ""  # Retorna True e uma string vazia quando os campos são válidos

    def _message(self, message: str, is_error: bool = True):
        """Exibe uma mensagem na tela"""
        if is_error:
            self.error_text.value = message
            self.error_text.visible = True
            self.success_text.visible = False
        else:
            self.success_text.value = message
            self.success_text.visible = True
            self.error_text.visible = False
        self.page.update()

    def _salvar_cliente(self, _):
        """Salva o cliente no banco de dados"""
        validar, message = self._validar_campos()
        if not validar:
            self._message(message, True)
            return
        user_id = Usuario.get_current_user()
        if user_id is None:
            self._message("Usuário não encontrado", True)
            return
        try:
            Cliente.create(
                user_id=user_id,
                nome=self.nome_input.value,
                cpf=self.cpf_input.value,
                telefone=self.telefone_input.value,
                email=self.email_input.value,
                endereco=self.endereco_input.value,
                cidade=self.cidade_input.value,
                estado=self.estado_input.value,
                cep=self.cep_input.value,
                bairro=self.bairro_input.value,
                numero=self.numero_input.value,
            )

            self._message(
                f"Cliente {self.nome_input.value} cadastrado com sucesso!", False
            )

            clientes = Cliente.list_by_user(user_id)
            for _cliente in clientes:
                if _cliente["telefone"] == self.telefone_input.value:
                    time.sleep(2)
                    menu_orc.mostrar_orcamento(self.page, _cliente)
                    return _cliente

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
                    ft.Text("Cadastro de Clientes", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.Colors.BLUE_GREY_100),
                    ft.Container(
                        content=ft.Column(
                            [
                                self.nome_input,
                                # self.cpf_input,
                                # self.data_nascimento_input,
                                # self.rg_input,
                                # self.email_input,
                                self.telefone_input,
                                # self.endereco_input,
                                # self.numero_input,
                                # self.bairro_input,
                                # self.cidade_input,
                                # self.estado_input,
                                # self.cep_input,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        **gsm.container_style,
                    ),
                    # ft.Divider(height=20, color=ft.Colors.BLUE_GREY_100),
                    self.error_text,
                    self.success_text,
                    ft.Row(
                        [
                            *self._create_buttons(),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=600,
            )
        )


def tela_cadastro_cliente(page: ft.Page):
    """Tela de cadastro de clientes"""
    page.controls.clear()
    cliente_page = Cadastro(page)
    page.add(cliente_page.build())
    page.update()
