"""Módulo para exibir detalhes de um cliente. App/Clientes/detalhes.py"""

import flet as ft

from base.orcamentos import menu_orc
from custom.styles_utils import get_style_manager

gsm = get_style_manager()


def detalhes_cliente(page: ft.Page, cliente):
    """Função para exibir os detalhes de um cliente"""
    from base.clientes.clientes import (
        tela_clientes,  # pylint: disable=import-outside-toplevel
    )

    page.controls.clear()
    page.add(
        ft.Column(
            controls=[
                ft.Text(f"Detalhes do Cliente: {cliente['nome']}", size=24),
                ft.Text(f"Telefone: {cliente['telefone']}"),
                ft.Text(f"Email: {cliente.get('email', 'Não informado')}"),
                ft.Text(f"Endereço: {cliente.get('endereco', 'Não informado')}"),
                ft.Row(
                    [
                        gsm.create_button(
                            text="Orçamento ",
                            on_click=lambda _,
                            cliente=cliente: menu_orc.mostrar_orcamento(page, cliente),
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
    page.update()
