"""Módulo para a tela de orçamentos. base/orcamentos/tela_orc.py"""

import datetime
# from typing import Optional

import flet as ft

from base.orcamentos import menu_orc
from custom.styles_utils import get_style_manager

from models.db import Orcamento

gsm = get_style_manager()


def criar_projeto(page: ft.Page, cliente):
    """Função para criar um novo projeto para um cliente."""
    page.controls.clear()
    page.add(ft.Text(f"Criar projeto para {cliente['nome']}", size=24))

    descricao_input = ft.TextField(label="Descrição do Projeto", **gsm.input_style)
    endereco_input = ft.TextField(label="Endereço do Projeto", **gsm.input_style)
    valor_input = ft.TextField(label="Valor (R$)", **gsm.input_style)
    valor_ = ft.TextField(label="Valor do Projeto", read_only=True, **gsm.input_style)

    def salvar_orcamento():
        """Função para salvar o orçamento no banco de dados."""
        descricao = descricao_input.value
        valor_total = float(valor_input.value)

        # Salvar no banco de dados
        Orcamento.adicionar_orcamento(
            cliente_id=cliente["id"],
            descricao=descricao,
            valor=valor_total,
            data_orcamento=datetime.datetime.now(),
        )

        # Exibir mensagem de sucesso
        page.add(ft.SnackBar(content=ft.Text("Orçamento criado com sucesso!")))
        page.update()

    salvar_button = ft.ElevatedButton(
        text="Salvar Orçamento", on_click=salvar_orcamento
    )
    btn_voltar = gsm.create_button(
        text="Voltar",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: menu_orc.mostrar_orcamento(page, cliente),
        width=130,
        hover_color=gsm.colors.VOLTAR,
    )

    page.add(
        descricao_input, endereco_input, valor_input, valor_, salvar_button, btn_voltar
    )
    page.update()
