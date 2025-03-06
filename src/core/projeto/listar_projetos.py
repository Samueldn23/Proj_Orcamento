"""Módulo para exibir detalhes de um cliente. App/Clientes/projetos.py"""

import flet as ft
import pytz

from src.core.projeto import criar_projeto
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import ClientRepository, ProjetoRepository

# Instanciar as classes dos repositórios
projeto_repo = ProjetoRepository()  # Criar instância
cliente_repo = ClientRepository()  # Criar instância

gsm = get_style_manager()


def projetos_cliente(page: ft.Page, cliente):
    """Função para exibir os projetos de um cliente"""
    try:
        # Modificar para usar o dicionário cliente corretamente
        cliente_id = cliente.get("id") if isinstance(cliente, dict) else cliente.id

        # Buscar projetos do cliente
        projetos_list = projeto_repo.list_by_client(cliente_id=cliente_id)

        from src.core.cliente.clientes import (
            tela_clientes,
        )

        def on_card_click(e, projeto):
            """Função para tratar o clique no card"""
            from src.core.projeto.detalhes_projeto import tela_detalhes_projeto

            tela_detalhes_projeto(page, projeto, cliente)

        def handle_hover(e, container):
            """Função para tratar o efeito hover"""
            if e.data == "true":  # Mouse entrou
                container.scale = 1.01
                container.shadow = ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=8,
                    # offset=ft.Offset(3, 3),
                    color=ft.Colors.LIGHT_BLUE_ACCENT,
                )
            else:  # Mouse saiu
                container.scale = 1.0
                container.shadow = ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    offset=ft.Offset(2, 2),
                )
            container.update()

        def criar_card_projeto(projeto):
            """Cria um card para exibir as informações do projeto"""
            # Converter para horário de Brasília
            tz_brasil = pytz.timezone("America/chicago")

            criado_em_br = projeto.criado_em.astimezone(tz_brasil)
            atualizado_em_br = projeto.atualizado_em.astimezone(tz_brasil)

            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"{projeto.nome}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            f"Descrição: {projeto.descricao or 'Não informada'}",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            f"Custo Estimado: R$ {projeto.custo_estimado or 0:.2f}",
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Criado em: {criado_em_br.strftime('%d/%m/%y %H:%M')}",
                                ),
                                ft.Text("|"),  # Separador
                                ft.Text(
                                    f"Atualizado em: {atualizado_em_br.strftime('%d/%m/%y %H:%M')}",
                                    size=12,
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                width=390,  # Largura fixa do container
                padding=10,
                border=ft.border.all(1, ft.Colors.LIGHT_BLUE_ACCENT_700),
                border_radius=10,
                margin=2,
                bgcolor=ft.Colors.BLACK,
                ink=True,  # Efeito de clique
                # Sombra para dar profundidade
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    offset=ft.Offset(2, 2),
                ),
                # Adiciona hover e clique
                on_click=lambda e: on_card_click(e, projeto),
                # Efeito hover
                animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                scale=1.0,
                on_hover=lambda e: handle_hover(e, card),
            )
            return card

        # Criar lista de cards de projetos
        projetos_cards = [criar_card_projeto(projeto) for projeto in projetos_list]

        # Se não houver projetos, mostrar mensagem
        if not projetos_cards:
            container = ft.Container(
                content=ft.Text(
                    "Nenhum projeto encontrado para este cliente.\n clique aqui para criar um novo projeto?",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=400,
                height=180,
                padding=10,
                border=ft.border.all(1, ft.Colors.LIGHT_BLUE_ACCENT_700),
                border_radius=10,
                margin=5,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.BLACK,
                ink=True,  # Efeito de clique
                # Sombra para dar profundidade
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    offset=ft.Offset(2, 2),
                ),
                # Adiciona hover e clique
                on_click=lambda _, cliente=cliente: criar_projeto.criar_projeto(page, cliente),
                # Efeito hover
                animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                scale=1.0,
                on_hover=lambda e: handle_hover(e, container),  # Passamos o container atual
            )
            projetos_cards = [container]

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
                                text="Novo Projeto",
                                on_click=lambda _, cliente=cliente: criar_projeto.criar_projeto(page, cliente),
                                icon=ft.Icons.ADD,
                                hover_color=gsm.colors.PRIMARY,
                            ),
                            gsm.create_button(
                                text="Voltar",
                                on_click=lambda _: tela_clientes(page),
                                icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                hover_color=gsm.colors.VOLTAR,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    # Adiciona um container para os cards de projetos em grid
                    ft.Container(
                        content=ft.Row(
                            controls=projetos_cards,
                            wrap=True,  # Permite quebra de linha
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        padding=3,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        page.update()
    except Exception as e:
        print(f"Erro ao listar projetos: {e}")
        # Mostrar mensagem de erro para o usuário
        page.open(ft.SnackBar(content=ft.Text("Erro ao carregar projetos"), bgcolor=ft.Colors.ERROR))
        return []
