"""Módulo para exibir e gerenciar detalhes de um projeto"""

import locale

import flet as ft

from src.core.projeto import listar_projetos
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.connections import Session
from src.infrastructure.database.models.construction import Wall
from src.infrastructure.database.repositories import ProjetoRepository
from src.navigation.router import navegar_orcamento

# Configuração da localização para formatação de moeda
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

gsm = get_style_manager()
projeto_repo = ProjetoRepository()
session = Session()


def criar_card_construcao(construcao):
    """Cria um card para exibir informações da construção"""
    return ft.Card(
        content=ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.HOUSE_SIDING, color=ft.Colors.BLUE, size=20),
                    ft.VerticalDivider(width=10),
                    ft.Column(
                        [
                            ft.Text(
                                f"Área: {construcao.area}m² - {construcao.tipo_tijolo}",
                                size=12,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"{construcao.quantidade_tijolos} tijolos",
                                        size=11,
                                        color=ft.Colors.BLUE_GREY_400,
                                    ),
                                    ft.Text(
                                        locale.currency(
                                            float(construcao.custo_total), grouping=True
                                        ),
                                        size=11,
                                        color=ft.Colors.GREEN,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.all(8),
        ),
        elevation=1,
    )


def tela_detalhes_projeto(page: ft.Page, projeto, cliente):
    """Função para exibir detalhes do projeto e opções de edição/exclusão"""

    def confirmar_exclusao(e):
        """Exibe diálogo de confirmação para exclusão"""

        def excluir_confirmado(e):
            dlg_confirmacao.open = False
            page.update()
            try:
                if projeto_repo.delete(projeto.id):
                    page.open(
                        ft.SnackBar(
                            content=ft.Text("Projeto excluído com sucesso!"),
                            bgcolor=ft.Colors.GREEN,
                        )
                    )
                    listar_projetos.projetos_cliente(page, cliente)
                else:
                    page.open(
                        ft.SnackBar(
                            content=ft.Text("Erro ao excluir projeto!"),
                            bgcolor=ft.Colors.ERROR,
                        )
                    )
            except Exception as error:
                page.open(
                    ft.SnackBar(
                        content=ft.Text(f"Erro ao excluir projeto: {str(error)}"),
                        bgcolor=ft.Colors.ERROR,
                    )
                )
            page.update()

        def cancelar_exclusao(e):
            dlg_confirmacao.open = False
            page.update()

        dlg_confirmacao = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(
                f"Deseja realmente excluir o projeto '{projeto.nome}'? \nEsta ação não poderá ser desfeita!"
            ),
            actions=[
                ft.TextButton("Sim", on_click=excluir_confirmado),
                ft.TextButton("Não", on_click=cancelar_exclusao),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg_confirmacao)
        dlg_confirmacao.open = True
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
                    content=ft.Text(f"Erro ao atualizar projeto: {str(error)}"),
                    bgcolor=ft.Colors.ERROR,
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
        # min_lines=3,
        # max_lines=5,
        **gsm.input_style,
    )
    valor_input = ft.TextField(
        label="Custo Estimado (R$)",
        value=str(projeto.custo_estimado) if projeto.custo_estimado else "",
        keyboard_type=ft.KeyboardType.NUMBER,
        **gsm.input_style,
    )

    # Adicionar lista de construções
    construcoes = session.query(Wall).filter_by(projeto_id=projeto.id).all()
    lista_construcoes = (
        ft.Column(
            [
                ft.Text("Construções", size=20, weight=ft.FontWeight.BOLD),
                ft.Column([criar_card_construcao(c) for c in construcoes]),
            ]
        )
        if construcoes
        else ft.Text("Nenhuma construção cadastrada")
    )

    page.window_width = 450
    page.window_height = 700
    page.window_resizable = False

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "Detalhes do Projeto",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_700,
                                ),
                                ft.Text(
                                    projeto.nome, size=16, color=ft.Colors.BLUE_GREY_700
                                ),
                            ],  # spacing=1
                        ),
                        padding=10,
                    ),
                    ft.Text(
                        f"Criado em: {projeto.criado_em.strftime('%d/%m/%Y')}",
                        color=ft.Colors.GREY_700,
                        size=12,
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLUE_100),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.TextField(
                                    ref=nome_input,
                                    label="Nome do Projeto",
                                    value=projeto.nome,
                                    prefix_icon=ft.Icons.FOLDER_SPECIAL,
                                    height=45,
                                    **gsm.input_style,
                                ),
                                ft.TextField(
                                    ref=descricao_input,
                                    label="Descrição",
                                    value=projeto.descricao,
                                    prefix_icon=ft.Icons.DESCRIPTION,
                                    multiline=True,
                                    min_lines=2,
                                    max_lines=3,
                                    **gsm.input_style,
                                ),
                                ft.TextField(
                                    ref=valor_input,
                                    label="Custo Estimado (R$)",
                                    prefix_icon=ft.Icons.ATTACH_MONEY,
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                    height=45,
                                    **gsm.input_style,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        gsm.create_button(
                                            text="Construir",
                                            icon=ft.Icons.ADD_HOME_WORK,
                                            on_click=lambda _: navegar_orcamento(
                                                page, cliente, projeto
                                            ),
                                            hover_color=ft.Colors.BLUE_700,
                                        ),
                                        gsm.create_button(
                                            text="Salvar",
                                            icon=ft.Icons.SAVE,
                                            on_click=salvar_edicao,
                                            hover_color=ft.Colors.GREEN_700,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                                ft.Row(
                                    [
                                        gsm.create_button(
                                            text="Excluir",
                                            icon=ft.Icons.DELETE_FOREVER,
                                            on_click=confirmar_exclusao,
                                            hover_color=ft.Colors.RED_700,
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
                                    spacing=10,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=ft.padding.symmetric(vertical=10),
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLUE_100),
                    ft.Container(
                        content=lista_construcoes,
                        padding=10,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=0,
            ),
            padding=10,
            border_radius=8,
        )
    )
    page.update()
