"""Módulo para a tela de orçamentos. base/orcamentos/tela_orc.py"""

import datetime
# from typing import Optional

import flet as ft
from src.core.cliente import projetos
from src.core.orcamento import menu_orc
from src.custom.styles_utils import get_style_manager

from src.infrastructure.database.repositories import (
    budget_repository,
    client_repository,
)

gsm = get_style_manager()

budget_repo = budget_repository.BudgetRepository()
client_repo = client_repository.ClientRepository()


def criar_projeto(page: ft.Page, cliente):
    """Função para criar um novo projeto para um cliente."""
    page.controls.clear()
    page.add(ft.Text(f"Criar projeto para {cliente['nome']}", size=24))

    descricao_input = ft.TextField(label="Descrição do Projeto", **gsm.input_style)
    endereco_input = ft.TextField(label="Endereço do Projeto", **gsm.input_style)
    valor_input = ft.TextField(label="Valor (R$)", read_only=True, **gsm.input_style)


    def salvar_orcamento():
        """Função para salvar o orçamento no banco de dados."""
        descricao = descricao_input.value
        valor_total = float(valor_input.value)

        # Salvar no banco de dados
        budget_repo.create(
            cliente_id=cliente["id"],
            data_orcamento=datetime.datetime.now(),
            descricao=descricao,
            valor=valor_total,
        )

        # Exibir mensagem de sucesso
        page.add(ft.SnackBar(content=ft.Text("Orçamento criado com sucesso!")))
        page.update()

    btn_orcamento = gsm.create_button(
        text="Orçamento",
        icon=ft.Icons.MONEY,
        on_click=lambda _: menu_orc.mostrar_orcamento(page, cliente),
        width=130,
        hover_color=gsm.colors.PRIMARY,
    )
    btn_voltar = gsm.create_button(
        text="Voltar",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: projetos.projetos_cliente(
                    page, cliente
                ),
        width=130,
        hover_color=gsm.colors.VOLTAR,
    )

    page.add(
        descricao_input, endereco_input, valor_input, btn_orcamento, btn_voltar
    )
    page.update()
