"""Pagina de configuração"""

import flet as ft
from sqlalchemy import create_engine

from src.core.configuracao.modulos import GerenciadorModulos
from src.custom.styles_utils import get_style_manager
from src.infrastructure.config.settings import settings
from src.infrastructure.database.migrations import create_tables
from src.infrastructure.database.models import Base
from src.navigation.router import navegar_principal

gsm = get_style_manager()


def atualizar_tabelas(e):
    """Função para atualizar as tabelas no banco de dados"""
    try:
        # Criar engine do SQLAlchemy usando a URL do banco
        engine = create_engine(settings.database_url)

        # Criar todas as tabelas definidas nos models
        Base.metadata.create_all(engine)
        create_tables.update_usuarios_table()
        create_tables.update_paredes_table()

        return True
    except Exception as error:
        print(f"Erro ao atualizar tabelas: {error}")
        return False


def tela_config(page):
    """Função de configuração"""
    page.controls.clear()
    page.title = "Configurações"

    # Inicializa o gerenciador de módulos
    gerenciador_modulos = GerenciadorModulos()
    gerenciador_modulos.carregar_modulos()  # Carrega estado atual dos módulos

    def handle_atualizar_click(e):
        """Handler para o clique no botão de atualizar"""
        sucesso = atualizar_tabelas(e)

        # Exibe mensagem de sucesso/erro
        page.open(
            ft.SnackBar(
                content=ft.Text("Tabelas atualizadas com sucesso!" if sucesso else "Erro ao atualizar tabelas!"),
                bgcolor=ft.Colors.GREEN if sucesso else ft.Colors.RED,
            )
        )
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Configurações do Sistema",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=20),
                # Seção de Banco de Dados
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Banco de Dados", size=18, weight=ft.FontWeight.BOLD),
                            gsm.create_button(
                                text="Atualizar Tabelas",
                                hover_color=ft.Colors.AMBER,
                                on_click=handle_atualizar_click,
                                icon=ft.Icons.UPDATE,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                    border_radius=10,
                ),
                # Seção de Módulos
                gerenciador_modulos.build(),  # Usa o novo gerenciador de módulos
                # Seção de Configurações da Empresa
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Dados da Empresa", size=18, weight=ft.FontWeight.BOLD),
                            ft.TextField(
                                label="Razão Social",
                                prefix_icon=ft.Icons.BUSINESS,
                                **gsm.input_style,
                            ),
                            ft.TextField(
                                label="CNPJ",
                                prefix_icon=ft.Icons.NUMBERS,
                                **gsm.input_style,
                            ),
                            ft.TextField(
                                label="Email",
                                prefix_icon=ft.Icons.EMAIL,
                                **gsm.input_style,
                            ),
                            ft.TextField(
                                label="Telefone",
                                prefix_icon=ft.Icons.PHONE,
                                **gsm.input_style,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                    border_radius=10,
                ),
                # Botão Voltar
                ft.Row(
                    [
                        gsm.create_button(
                            text="Voltar",
                            on_click=lambda e: navegar_principal(page),
                            icon=ft.Icons.ARROW_BACK,
                            hover_color=gsm.colors.VOLTAR,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        ft.Divider(height=20),
    )
    page.update()
