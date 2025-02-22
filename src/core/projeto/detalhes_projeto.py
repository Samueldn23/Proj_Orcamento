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
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.icons.WALL),
                    title=ft.Text(f"Parede {construcao.id}"),
                    subtitle=ft.Text(f"Área: {construcao.area}m² | Tipo: {construcao.tipo_tijolo}")
                ),
                ft.Row([
                    ft.Text(f"Tijolos: {construcao.quantidade_tijolos} un"),
                    ft.Text(f"Custo: {locale.currency(float(construcao.custo_total), grouping=True)}")
                ]),
            ]),
            padding=10
        )
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

        def cancelar_exclusao(e):
            dlg_confirmacao.open = False
            page.update()

        dlg_confirmacao = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir o projeto '{projeto.nome}'? \nEsta ação não poderá ser desfeita!"),
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

    # Adicionar lista de construções
    construcoes = session.query(Wall).filter_by(orcamento_id=projeto.id).all()
    lista_construcoes = ft.Column([
        ft.Text("Construções", size=20, weight=ft.FontWeight.BOLD),
        ft.Column([criar_card_construcao(c) for c in construcoes])
    ]) if construcoes else ft.Text("Nenhuma construção cadastrada")

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
                            on_click=lambda _: navegar_orcamento(
                                page, cliente, projeto
                            ),
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
                            on_click=confirmar_exclusao,
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
                ft.Divider(),
                lista_construcoes,
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
    page.update()
