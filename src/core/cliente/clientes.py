"""Módulo para gerenciar os clientes. base/Clientes/clientes.py"""

import flet as ft

from src.infrastructure.database.repositories import user_repository, client_repository

from src.core.cliente import atualizar, cadastrar, projetos
from src.navigation.router import navegar_principal
from src.custom.styles_utils import get_style_manager

gsm = get_style_manager()
user_repo = user_repository.UserRepository()
client_repo = client_repository.ClientRepository()


def tela_clientes(page):
    """Função principal do aplicativo"""
    page.controls.clear()
    page.title = "Listar Clientes"
    largura = 150

    def listar_clientes():
        """Função para listar clientes"""
        user_id = (
            user_repo.get_current_user()
        )  # Substitua pelo ID do usuário autenticado
        clientes = client_repo.list_by_user(user_id)

        if not clientes:
            page.add(ft.Text("Nenhum cliente encontrado.", color="red", size=20))
            page.update()
            return

        # Criar o cabeçalho da lista
        lista_clientes = [
            ft.Row(
                controls=[
                    ft.Text("Nome", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Telefone", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Ações", size=18, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]

        # Adicionar clientes à lista
        for cliente in clientes:
            lista_clientes.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(cliente["nome"], size=16, width=largura),
                            on_click=lambda e,
                            cliente=cliente: projetos.projetos_cliente(page, cliente),
                        ),
                        ft.Container(
                            content=ft.Text(
                                cliente["telefone"], size=16, width=largura
                            ),
                            on_click=lambda e,
                            cliente=cliente: projetos.projetos_cliente(page, cliente),
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_size=20,
                                    on_click=lambda e, cliente=cliente: editar_cliente(
                                        cliente
                                    ),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=20,
                                    on_click=lambda e, cliente=cliente: excluir_cliente(
                                        cliente
                                    ),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    height=40,
                ),
            )

        # Adicionar o ListView com rolagem automática
        lista_clientes_scrollable = ft.ListView(
            controls=lista_clientes,
            auto_scroll=True,
            height=500,
            width=page.width - 40,
        )

        page.add(lista_clientes_scrollable)
        page.update()

    def editar_cliente(cliente_id):
        """Função para editar cliente"""
        atualizar.tela_editar_cliente(page, cliente_id)

    def excluir_cliente(cliente_id):
        """Função para excluir cliente"""
        cliente_id = cliente_id["id"]
        print(f"Excluindo cliente com ID: {cliente_id}")
        client_repo.deletar_cliente(cliente_id)
        listar_clientes()

    # Cabeçalho moderno e estilizado
    page.add(
        ft.Row(
            [
                ft.Icon(ft.Icons.PERSON, size=30, color="blue"),
                ft.Text("Gestão de Clientes", size=28, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        ft.Divider(height=10, color="grey"),
        ft.Row(
            [
                gsm.create_button(
                    text="",
                    on_click=lambda e: cadastrar.tela_cadastro_cliente(page),
                    icon=ft.Icons.ADD,
                    width=34,
                    hover_color=gsm.colors.PRIMARY,
                ),
                gsm.create_button(
                    text="",
                    on_click=lambda e: navegar_principal(page),
                    icon=ft.Icons.ARROW_BACK,
                    width=34,
                    hover_color=gsm.colors.VOLTAR,
                ),
                ft.TextField(icon=ft.Icons.SEARCH,)

            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    # Chamar a função de listagem de clientes diretamente ao carregar a página
    listar_clientes()
    page.update()
