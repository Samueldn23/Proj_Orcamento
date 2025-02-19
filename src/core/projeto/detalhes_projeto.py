"""Módulo para exibir e gerenciar detalhes de um projeto"""

import flet as ft
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import ProjetoRepository
from src.core.projeto import listar_projetos
from src.core.orcamento.menu_orc import mostrar_orcamento

gsm = get_style_manager()
projeto_repo = ProjetoRepository()


def tela_detalhes_projeto(page: ft.Page, projeto, cliente):
    """Função para exibir detalhes do projeto e opções de edição/exclusão"""

    def confirmar_exclusao():
        """Função para confirmar exclusão do projeto"""
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Tem certeza que deseja excluir este projeto?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: dlg.open),
                ft.TextButton("Excluir", on_click=excluir_projeto),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def excluir_projeto(e):
        """Função para excluir o projeto"""
        try:
            if projeto_repo.delete(projeto.id):
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Projeto excluído com sucesso!"),
                        bgcolor=ft.colors.GREEN,
                    )
                )
                listar_projetos.projetos_cliente(page, cliente)
            else:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Erro ao excluir projeto!"),
                        bgcolor=ft.colors.ERROR,
                    )
                )
        except Exception as error:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao excluir projeto: {str(error)}"),
                    bgcolor=ft.colors.ERROR,
                )
            )
        page.update()

    def salvar_edicao(e):
        """Função para salvar as alterações no projeto"""
        try:
            if not nome_input.value:
                page.open(
                    ft.SnackBar(content=ft.Text("Nome do projeto é obrigatório!"))
                )
                return

            custo_estimado = float(valor_input.value) if valor_input.value else None

            projeto_atualizado = projeto_repo.update(
                projeto_id=projeto.id,
                nome=nome_input.value,
                descricao=descricao_input.value,
                custo_estimado=custo_estimado,
            )

            if projeto_atualizado:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Projeto atualizado com sucesso!"),
                        bgcolor=ft.Colors.GREEN,
                    )
                )
                listar_projetos.projetos_cliente(page, cliente)
            else:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Erro ao atualizar projeto!"),
                        bgcolor=ft.colors.ERROR,
                    )
                )
        except ValueError:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Valor inválido para o custo estimado!"),
                    bgcolor=ft.colors.ERROR,
                )
            )
        except Exception as error:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao atualizar projeto: {str(error)}"),
                    bgcolor=ft.colors.ERROR,
                )
            )
        page.update()

    # Campos de edição
    nome_input = ft.TextField(
        label="Nome do Projeto", value=projeto.nome, **gsm.input_style
    )
    descricao_input = ft.TextField(
        label="Descrição",
        value=projeto.descricao,
        multiline=True,
        min_lines=3,
        max_lines=5,
        **gsm.input_style,
    )
    valor_input = ft.TextField(
        label="Custo Estimado (R$)",
        value=str(projeto.custo_estimado) if projeto.custo_estimado else "",
        keyboard_type=ft.KeyboardType.NUMBER,
        **gsm.input_style,
    )

    dlg = confirmar_exclusao()
    page.dialog = dlg

    page.controls.clear()
    page.add(
        ft.Column(
            controls=[
                ft.Text(f"Detalhes do Projeto: {projeto.nome}", size=24),
                ft.Text(f"Criado em: {projeto.criado_em.strftime('%d/%m/%Y')}"),
                ft.Divider(),
                nome_input,
                descricao_input,
                valor_input,
                ft.Row(
                    [
                        gsm.create_button(
                            text="Orçamento",
                            icon=ft.Icons.PLUS_ONE,
                            on_click=lambda _: mostrar_orcamento(page, cliente),
                            hover_color=ft.Colors.BLUE,                            
                        ),
                        gsm.create_button(
                            text="Salvar",
                            icon=ft.Icons.SAVE,
                            on_click=salvar_edicao,
                            hover_color=ft.Colors.GREEN,
                        ),
                        gsm.create_button(
                            text="Excluir",
                            icon=ft.Icons.DELETE,
                            on_click=lambda _: dlg.open,
                            hover_color=ft.Colors.RED,
                        ),
                        gsm.create_button(
                            text="Voltar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: listar_projetos.projetos_cliente(
                                page, cliente
                            ),
                            hover_color=gsm.colors.VOLTAR,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    )
    page.update()
