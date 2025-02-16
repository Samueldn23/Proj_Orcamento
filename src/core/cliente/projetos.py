"""Módulo para exibir detalhes de um cliente. App/Clientes/projetos.py"""

import flet as ft

from src.core.orcamento import index_orcamento
from src.custom.styles_utils import get_style_manager

gsm = get_style_manager()


def projetos_cliente(page: ft.Page, cliente):
    """Função para exibir os projetos de um cliente"""
    from src.core.cliente.clientes import (  # pylint: disable=import-outside-toplevel
        tela_clientes,
    )

    def listar_projetos():
        """Função para listar os projetos de um cliente"""

    page.controls.clear()
    page.add(
        ft.Column(
            controls=[
                ft.Text(f"Projetos do Cliente: {cliente['nome']}", size=24),
                ft.Text(f"Telefone: {cliente['telefone']}"),
                ft.Text(f"Email: {cliente.get('email', 'Não informado')}"),
                ft.Text(f"Endereço: {cliente.get('endereco', 'Não informado')}"),
                ft.Row(
                    [
                        gsm.create_button(
                            text="Projeto",
                            on_click=lambda _,
                            cliente=cliente: index_orcamento.criar_projeto(
                                page, cliente
                            ),
                            icon=ft.Icons.ADD,
                            hover_color=gsm.colors.PRIMARY,
                        ),
                        gsm.create_button(
                            text="Voltar ",
                            on_click=lambda _: tela_clientes(page),
                            icon=ft.Icons.ARROW_BACK_IOS_NEW,
                            hover_color=gsm.colors.VOLTAR,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    listar_projetos()
    page.update()
