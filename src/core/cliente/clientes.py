"""Módulo para gerenciar os clientes. base/Clientes/clientes.py"""

import flet as ft

from src.core.cliente import atualizar, cadastrar
from src.core.projeto import listar_projetos
from src.custom.styles_utils import get_style_manager
from src.infrastructure.cache.cache_config import clear_cache
from src.infrastructure.database.repositories import client_repository, user_repository
from src.navigation.router import navegar_principal

gsm = get_style_manager()
user_repo = user_repository.UserRepository()
client_repo = client_repository.ClientRepository()

# Variável global para armazenar todos os clientes
todos_clientes = []


def formatar_telefone(telefone: str) -> str:
    """Formata o número de telefone para o padrão (XX) X XXXX-XXXX"""
    if not telefone:
        return ""

    # Remove todos os caracteres não numéricos
    numeros = "".join(filter(str.isdigit, telefone))

    # Verifica se é um número de celular (11 dígitos) ou fixo (10 dígitos)
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:3]} {numeros[3:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"

    return telefone


def editar_cliente(cliente, page=None):
    """Função para editar cliente"""
    if page:
        atualizar.tela_editar_cliente(page, cliente)


def excluir_cliente(cliente, page=None):
    """Função para excluir cliente"""
    if not page:
        return

    cliente_id = cliente["id"]
    print(f"Excluindo cliente com ID: {cliente_id}")

    # Tenta excluir o cliente
    if client_repo.delete(cliente_id):
        print(f"Cliente {cliente_id} excluído com sucesso!")
        # Limpa o cache
        clear_cache()
        print("Cache limpo após exclusão do cliente")

        # Limpa a tela antes de recarregar
        page.controls.clear()

        # Adiciona o cabeçalho novamente
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
                    ft.TextField(
                        label="Pesquisar",
                        icon=ft.Icons.SEARCH,
                        on_change=lambda e: filtrar_clientes(e, page),
                        hint_text="Digite para pesquisar...",
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        # Atualiza a lista de clientes
        listar_clientes(page)

        # Mostra mensagem de sucesso
        page.open(
            ft.SnackBar(
                content=ft.Text("Cliente excluído com sucesso!"),
                bgcolor=ft.Colors.GREEN,
            )
        )
    else:
        print(f"Erro ao excluir cliente {cliente_id}")
        # Mostra mensagem de erro
        page.open(
            ft.SnackBar(
                content=ft.Text("Erro ao excluir cliente. Tente novamente."),
                bgcolor=ft.Colors.ERROR,
            )
        )
    page.update()


def atualizar_lista_clientes(page: ft.Page, clientes: list, largura: int = 150):
    """Atualiza a lista de clientes na tela"""
    # Remove a lista antiga se existir
    for control in page.controls[:]:
        if isinstance(control, ft.ListView):
            page.controls.remove(control)

    if not clientes:
        # Se não houver clientes, mostra a mensagem
        for control in page.controls[:]:
            if isinstance(control, ft.Text) and control.color == "red":
                page.controls.remove(control)
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
        # Formata o telefone antes de exibir
        telefone_formatado = formatar_telefone(cliente["telefone"])

        lista_clientes.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(cliente["nome"], size=16, width=largura),
                        on_click=lambda e, cliente=cliente: listar_projetos.projetos_cliente(page, cliente),
                    ),
                    ft.Container(
                        content=ft.Text(telefone_formatado, size=16, width=largura),
                        on_click=lambda e, cliente=cliente: listar_projetos.projetos_cliente(page, cliente),
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_size=20,
                                on_click=lambda e, cliente=cliente: editar_cliente(cliente, page),
                                style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_size=20,
                                on_click=lambda e, cliente=cliente: excluir_cliente(cliente, page),
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


def filtrar_clientes(e, page: ft.Page):
    """Filtra os clientes com base no texto digitado"""
    texto_pesquisa = e.control.value.lower()
    clientes_filtrados = [
        cliente for cliente in todos_clientes if texto_pesquisa in cliente["nome"].lower() or texto_pesquisa in (cliente["telefone"] or "").lower()
    ]
    atualizar_lista_clientes(page, clientes_filtrados)


def listar_clientes(page):
    """Função para listar clientes"""
    global todos_clientes
    # Limpa o cache antes de buscar os clientes
    clear_cache()

    # Obtém o ID do usuário atual
    user_id = user_repo.get_current_user()

    # Busca os clientes do usuário
    todos_clientes = client_repo.list_by_user(user_id)
    atualizar_lista_clientes(page, todos_clientes)


def tela_clientes(page):
    """Função principal do aplicativo"""
    global todos_clientes
    page.controls.clear()
    page.title = "Listar Clientes"

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
                ft.TextField(
                    label="Pesquisar",
                    icon=ft.Icons.SEARCH,
                    on_change=lambda e: filtrar_clientes(e, page),
                    hint_text="Digite para pesquisar...",
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    # Chamar a função de listagem de clientes diretamente ao carregar a página
    listar_clientes(page)
    page.update()
