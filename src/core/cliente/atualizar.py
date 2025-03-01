"""Módulo para a tela de edição de cadastro do cliente. atuualizar.py"""

import flet as ft

from src.core.cliente import clientes
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import ClientRepository, UserRepository

gsm = get_style_manager()
Usuario = UserRepository()
Cliente = ClientRepository()


def tela_editar_cliente(page, cliente):
    """Tela de edição de cadastro do cliente"""

    # Limpar a tela anterior
    page.controls.clear()

    page.title = "Editar Cliente"
    page.padding = 0
    # Dados do cliente
    cliente_id = cliente["id"]
    user_id = cliente["user_id"]

    # Criar campos de entrada para edição
    inputs = [
        ft.TextField(label="Nome", value=cliente["nome"], height=50, **gsm.input_style),
        ft.TextField(label="CPF", value=cliente["cpf"], height=50, **gsm.input_style),
        ft.TextField(
            label="Telefone",
            value=cliente["telefone"],
            height=50,
            **gsm.input_style,
        ),
        ft.TextField(
            label="Email",
            value=cliente["email"],
            height=50,
            **gsm.input_style,
        ),
        ft.TextField(
            label="Endereço",
            value=cliente["endereco"],
            height=50,
            **gsm.input_style,
        ),
        ft.TextField(
            label="Cidade",
            value=cliente["cidade"],
            height=50,
            **gsm.input_style,
        ),
        ft.TextField(
            label="Estado",
            value=cliente["estado"],
            height=50,
            **gsm.input_style,
        ),
        ft.TextField(label="CEP", value=cliente["cep"], height=50, **gsm.input_style),
        ft.TextField(
            label="Bairro",
            value=cliente["bairro"],
            height=50,
            **gsm.input_style,
        ),
        ft.TextField(
            label="Número",
            value=cliente["numero"],
            height=50,
            **gsm.input_style,
        ),
    ]

    @staticmethod
    # Função para salvar alterações
    def salvar_alteracoes(_):
        cliente_atualizado = {
            "id": cliente_id,
            "user_id": user_id,
            "nome": inputs[0].value.strip(),
            "cpf": inputs[1].value.strip(),
            "telefone": inputs[2].value.strip(),
            "email": inputs[3].value.strip(),
            "endereco": inputs[4].value.strip(),
            "cidade": inputs[5].value.strip(),
            "estado": inputs[6].value.strip(),
            "cep": inputs[7].value.strip(),
            "bairro": inputs[8].value.strip(),
            "numero": inputs[9].value.strip(),
        }

        # Atualizar cliente no banco de dados
        sucesso = Cliente.update(cliente_id, cliente_atualizado)

        # Configura e exibe o SnackBar
        page.open(
            ft.SnackBar(
                content=ft.Text(
                    "Cliente atualizado com sucesso!"
                    if sucesso
                    else "Erro ao atualizar cliente!"
                ),
                bgcolor=ft.Colors.GREEN if sucesso else ft.Colors.RED,
            )
        )
        clientes.tela_clientes(page)

    # Função para cancelar edição
    def cancelar_edicao(_):
        page.controls.clear()
        clientes.tela_clientes(page)  # Retorna para a tela de listagem de clientes

    # Adicionar componentes na ListView
    page.add(
        ft.Column(
            [
                ft.Text(
                    "Editar Cadastro do Cliente",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(
                    content=ft.ListView(
                        controls=inputs,
                        expand=True,
                        spacing=20,
                    ),
                    **gsm.container_style,
                ),
                ft.Row(
                    [
                        gsm.create_button(
                            "Salvar",
                            on_click=salvar_alteracoes,
                            width=120,
                            icon=ft.Icons.SAVE_ALT,
                            hover_color="green",
                        ),
                        gsm.create_button(
                            "Cancelar",
                            on_click=cancelar_edicao,
                            width=150,
                            icon=ft.Icons.CANCEL,
                            hover_color=gsm.colors.VOLTAR,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ],
            spacing=20,
        )
    )
    page.update()
