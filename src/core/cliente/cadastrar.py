"""Modulo de cadastro de clientes. cadastro.py"""

import time

import flet as ft

from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import ClientRepository, UserRepository

gsm = get_style_manager()
Cliente = ClientRepository()
Usuario = UserRepository()


def formatar_telefone(telefone: str) -> str:
    """Formata o número de telefone para o padrão (XX) X XXXX-XXXX"""
    if not telefone:
        return ""

    # Remove todos os caracteres não numéricos
    numeros = "".join(filter(str.isdigit, telefone))

    # Verifica se é um número de celular (11 dígitos) ou fixo (10 dígitos)
    if len(numeros) == 12:
        return f"({numeros[:2]}) {numeros[2:3]} {numeros[3:7]}-{numeros[7:]}"
    elif len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"

    return telefone


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
            helper_text="Digite seu telefone (Ex: 61999999999)",
            keyboard_type=ft.KeyboardType.PHONE,
            on_change=self._formatar_telefone_input,
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

    def _formatar_telefone_input(self, e):
        """Formata o telefone enquanto o usuário digita"""
        if e.data:  # Se houver dados
            # Remove formatação atual
            numeros = "".join(filter(str.isdigit, e.data))
            # Limita a 11 dígitos
            numeros = numeros[:12]
            # Formata e atualiza o campo
            self.telefone_input.value = formatar_telefone(numeros)
            self.page.update()

    def _validar_campos(self) -> tuple[bool, str]:
        """Valida os campos do formulário"""
        if not self.nome_input.value:
            self._message("O campo nome é obrigatório", True)
            return False, "O campo nome é obrigatório"

        if not self.telefone_input.value:
            self._message("O campo telefone é obrigatório", True)
            return False, "O campo telefone é obrigatório"

        # Valida o formato do telefone
        numeros = "".join(filter(str.isdigit, self.telefone_input.value))
        if len(numeros) < 10:
            self._message("Telefone inválido. Digite pelo menos 10 números.", True)
            return False, "Telefone inválido"

        return True, ""

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
            # Remove a formatação do telefone antes de salvar
            telefone = "".join(filter(str.isdigit, self.telefone_input.value))

            Cliente.create(
                user_id=user_id,
                nome=self.nome_input.value,
                cpf=self.cpf_input.value if hasattr(self, "cpf_input") else None,
                telefone=telefone,
                email=self.email_input.value if hasattr(self, "email_input") else None,
                endereco=self.endereco_input.value if hasattr(self, "endereco_input") else None,
                cidade=self.cidade_input.value if hasattr(self, "cidade_input") else None,
                estado=self.estado_input.value if hasattr(self, "estado_input") else None,
                cep=self.cep_input.value if hasattr(self, "cep_input") else None,
                bairro=self.bairro_input.value if hasattr(self, "bairro_input") else None,
                numero=self.numero_input.value if hasattr(self, "numero_input") else None,
            )

            self._message(f"Cliente {self.nome_input.value} cadastrado com sucesso!", False)

            # Aguarda 2 segundos para mostrar a mensagem de sucesso
            time.sleep(2)

            # Redireciona para a tela de clientes
            from src.core.cliente import clientes

            clientes.tela_clientes(self.page)
            return

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
