"""Módulo para a tela de orçamentos. base/orcamentos/tela_orc.py"""

# import datetime
# from typing import Optional

import flet as ft

from src.core.projeto import listar_projetos
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import (
    client_repository,
    projeto_repository,
)

gsm = get_style_manager()

projeto_repo = projeto_repository.ProjetoRepository()
client_repo = client_repository.ClientRepository()


def criar_projeto(page, cliente):
    """Função para criar um novo projeto para um cliente."""
    page.controls.clear()
    page.add(ft.Text(f"Criar projeto para {cliente['nome']}", size=24))

    nome_input = ft.TextField(label="Nome do Projeto", **gsm.input_style)
    descricao_input = ft.TextField(label="Descrição do Projeto", **gsm.input_style)
    endereco_input = ft.TextField(label="Endereço do Projeto", **gsm.input_style)
    valor_input = ft.TextField(
        label="Custo Estimado (R$)",
        keyboard_type=ft.KeyboardType.NUMBER,
        **gsm.input_style,
    )

    def salvar_projeto(e):
        """Função para salvar o projeto no banco de dados."""
        try:
            # Validar campos obrigatórios
            if not nome_input.value:
                page.open(
                    ft.SnackBar(content=ft.Text("Nome do projeto é obrigatório!"))
                )
                return

            # Converter valor para float se existir
            custo_estimado = float(valor_input.value) if valor_input.value else None

            # Criar novo projeto
            novo_projeto = projeto_repo.create(
                nome=nome_input.value,
                cliente_id=cliente["id"],
                descricao=descricao_input.value,
                custo_estimado=custo_estimado,
            )

            if novo_projeto:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Projeto criado com sucesso!"),
                        bgcolor=ft.Colors.GREEN,
                    )
                )
                # Redirecionar para a lista de projetos do cliente
                listar_projetos.projetos_cliente(page, cliente)
            else:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Erro ao criar projeto!"),
                        bgcolor=ft.Colors.ERROR,
                    )
                )

        except ValueError:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Valor inválido para o custo estimado!"),
                    bgcolor=ft.Colors.ERROR,
                )
            )
        except Exception as error:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao criar projeto: {error!s}"),
                    bgcolor=ft.Colors.ERROR,
                )
            )
        page.update()

    btn_voltar = gsm.create_button(
        text="Voltar",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: listar_projetos.projetos_cliente(page, cliente),
        hover_color=gsm.colors.VOLTAR,
    )

    btn_salvar = gsm.create_button(
        text="Salvar Projeto",
        icon=ft.Icons.SAVE,
        on_click=salvar_projeto,  # Corrigido para passar a função diretamente
        hover_color=ft.Colors.GREEN,
    )

    page.add(
        nome_input,
        descricao_input,
        endereco_input,
        valor_input,
        ft.Row(
            [btn_salvar, btn_voltar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
    page.update()
