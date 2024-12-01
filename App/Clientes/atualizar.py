"""Módulo para a tela de edição de cadastro do cliente. atuualizar.py"""

import flet as ft
from custom.styles_utils import get_style_manager
from models.db import Cliente
from App.Clientes import clientes

gsm = get_style_manager()


def tela_editar_cliente(page, cliente):
    """Tela de edição de cadastro do cliente"""

    # Limpar a tela anterior
    page.controls.clear()

    page.title = "Editar Cliente"
    # page.padding = 20
    page.scroll = "adaptive"  # Permite rolagem quando o conteúdo ultrapassar a altura
    # Dados do cliente
    cliente_id = cliente["id"]
    user_id = cliente["user_id"]

    # Criar campos de entrada para edição
    inputs = [
        ft.TextField(label="Nome", value=cliente["nome"], width=400, height=50),
        ft.TextField(label="CPF", value=cliente["cpf"], width=400, height=50),
        ft.TextField(label="Telefone", value=cliente["telefone"], width=400, height=50),
        ft.TextField(label="Email", value=cliente["email"], width=400, height=50),
        ft.TextField(label="Endereço", value=cliente["endereco"], width=400, height=50),
        ft.TextField(label="Cidade", value=cliente["cidade"], width=400, height=50),
        ft.TextField(label="Estado", value=cliente["estado"], width=400, height=50),
        ft.TextField(label="CEP", value=cliente["cep"], width=400, height=50),
        ft.TextField(label="Bairro", value=cliente["bairro"], width=400, height=50),
        ft.TextField(label="Número", value=cliente["numero"], width=400, height=50),
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
        sucesso = Cliente.atualizar_cliente(cliente_id, cliente_atualizado)

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
                ),
                ft.ListView(
                    controls=inputs,
                    expand=True,
                    spacing=20,
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
                            icon=ft.Icons.CIRCLE_OUTLINED,
                            hover_color=gsm.colors.VOLTAR,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            spacing=20,
        )
    )
    page.update()
