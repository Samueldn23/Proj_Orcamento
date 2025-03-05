"""Importações necessárias para o funcionamento do menu principal. menu.py"""

# 1. Módulos padrão
from collections.abc import Callable

# 2. Módulos de terceiros
import flet as ft

from _tests import teste_btn
from examples import exemplos

# 3. Módulos locais
from src.core.cliente import clientes

# from base.SPDA import SPDA
from src.core.configuracao import configuracao
from src.core.empresa import empresa
from src.custom.styles_utils import get_style_manager
from src.infrastructure.database.repositories import UserRepository
from src.navigation.router import navigate_to_login  # Nova importação

gsm = get_style_manager()
Usuario = UserRepository()  # Instanciar o repositório


class MenuButton(ft.ElevatedButton):
    """Classe personalizada para botões do menu principal"""

    def __init__(self, text: str, on_click: Callable, width: int = 200):
        super().__init__(
            text=text,
            on_click=on_click,
            width=width,
        )


class MenuPrincipalPage:
    """Classe para gerenciar a página do menu principal"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.user_info = self._get_user_info()
        self._init_buttons()

    def _get_user_info(self):
        """Obtém informações do usuário atual"""
        try:
            self.user_id = Usuario.get_current_user()
            self.user_data = Usuario.get_by_id(self.user_id) if self.user_id else None

            # Obtém o nome do usuário
            self.user_name = self.user_data.nome if self.user_data else "Usuário"

            # Obtém o email do usuário atual usando o Supabase Auth
            self.user_email = None
            try:
                self.user_email = Usuario.get_user_email()
                print(f"Email obtido: {self.user_email}")
            except Exception as e:
                print(f"Erro ao obter email: {e}")

            # Cria a informação de exibição do usuário com nome e email
            if self.user_email:
                self.user_display = f"{self.user_name} ({self.user_email})"
            else:
                self.user_display = self.user_name
                print("Email não disponível, usando apenas o nome")

            # Verifica se é o primeiro acesso
            if self.user_id:
                self.modulos = Usuario.get_modules(self.user_id)
            else:
                self.modulos = None

            return {"nome": self.user_name}
        except Exception as e:
            print(f"Erro ao obter informações do usuário: {e}")
            self.user_display = "Usuário"
            return {"nome": "Usuário"}

    def _init_buttons(self):
        """Inicializa os botões do menu principal"""
        self.menu_items = [
            {
                "text": "Clientes",
                "action": clientes.tela_clientes,
                "icon": ft.Icons.PEOPLE,
                "color": ft.Colors.CYAN_400,
            },
            {
                "text": "Empresa",
                "action": empresa.tela_cadastro_empresa,
                "icon": ft.Icons.BUSINESS,
                "color": ft.Colors.INDIGO_400,
            },
            {
                "text": "Exemplo",
                "action": exemplos.mostrar_parede,
                "icon": ft.Icons.VIEW_QUILT,
                "color": ft.Colors.TEAL_400,
            },
            {
                "text": "Teste Butões",
                "action": teste_btn.main,
                "icon": ft.Icons.TOUCH_APP,
                "color": ft.Colors.AMBER_400,
            },
            {
                "text": "Configuração",
                "action": configuracao.tela_config,
                "icon": ft.Icons.SETTINGS,
                "color": ft.Colors.PURPLE_400,
            },
        ]

        # Cria os botões do menu
        self.menu_buttons = [self._create_menu_button(item) for item in self.menu_items]

    def _handle_logout(self, _):
        """Função para lidar com o logout"""
        print("Tentando fazer logout...")
        try:
            # Obtém o ID do usuário atual antes do logout
            user_id_before = Usuario.get_current_user()
            print(f"Usuário antes do logout: {user_id_before}")

            logout_success = Usuario.logout()
            print(f"Resultado do logout: {logout_success}")

            # Verifica novamente o ID do usuário após o logout
            user_id_after = Usuario.get_current_user()
            print(f"Usuário após o logout: {user_id_after}")

            # Força o redirecionamento independente do resultado
            print("Redirecionando para tela de login")

            # Limpar completamente a página e reconstruir a tela de login
            self.page.controls.clear()
            from src.user.login import LoginPage

            # Cria uma nova instância da página de login
            login_page = LoginPage(self.page)
            self.page.add(login_page.build())
            self.page.update()

        except Exception as e:
            print(f"Exceção durante o logout: {e}")
            self.page.open(ft.SnackBar(content=ft.Text(f"Erro inesperado: {e}"), bgcolor=ft.Colors.ERROR))

    def _create_menu_button(self, item: dict) -> ft.Container:
        """Cria um botão de menu estilizado"""
        return gsm.create_button(
            text=item["text"],
            on_click=lambda _: item["action"](self.page),
            width=200,
            icon=item.get("icon"),
            hover_color=item.get("color", ft.Colors.BLUE),
            text_color=ft.Colors.WHITE,
            icon_color=item.get("color", ft.Colors.BLUE),
        )

    def build(self):
        """Constrói o layout do menu principal"""
        # Aplicar tema de fundo escuro
        self.page.bgcolor = ft.Colors.GREY_900

        # Logotipo e cabeçalho
        logo = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        name=ft.Icons.ANALYTICS_ROUNDED,
                        size=40,
                        color=ft.Colors.CYAN_400,
                    ),
                    ft.Text(
                        "Sistema de Orçamentos",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.CYAN_300,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            margin=ft.margin.only(top=20, bottom=10),
        )

        # Card de informações do usuário
        user_avatar = ft.CircleAvatar(
            content=ft.Text(
                self.user_name[0].upper() if self.user_name else "U",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            bgcolor=ft.Colors.BLUE_700,
            radius=20,
        )

        user_container = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                user_avatar,
                                ft.Column(
                                    [
                                        ft.Text(
                                            self.user_name,
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_700,
                                        ),
                                        ft.Text(
                                            self.user_email or "Email não disponível",
                                            size=12,
                                            color=ft.Colors.BLUE_GREY_700,
                                        ),
                                    ],
                                    spacing=0,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=15,
                        ),
                    ]
                ),
                padding=ft.padding.all(15),
                width=400,
            ),
            elevation=2,
            margin=ft.margin.only(bottom=20),
        )

        # Botões do menu em um grid
        menu_grid = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    [button],
                    col={"sm": 12, "md": 6, "lg": 4, "xl": 3},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
                for button in self.menu_buttons
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # Botão de logout estilizado
        logout_button = gsm.create_button(
            "Sair",
            on_click=self._handle_logout,
            width=120,
            icon=ft.icons.LOGOUT,
            hover_color=ft.Colors.RED_500,
            text_color=ft.Colors.WHITE,
        )

        # Rodapé
        footer = ft.Container(
            content=ft.Row(
                [
                    ft.Text("© 2025 - Sistema de Orçamentos", size=12, color=ft.Colors.BLUE_GREY_700),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            margin=ft.margin.only(top=20),
        )

        # Container principal com efeito de sombra
        return ft.Container(
            content=ft.Column(
                controls=[
                    logo,
                    user_container,
                    ft.Divider(height=1, color=ft.Colors.BLUE_GREY_200),
                    ft.Container(
                        content=menu_grid,
                        margin=ft.margin.only(top=20, bottom=20),
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLUE_GREY_200),
                    logout_button,
                    footer,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=600,
            padding=ft.padding.all(20),
            border_radius=10,
            bgcolor=ft.Colors.GREY_900,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
            margin=ft.margin.all(20),
        )


def mostrar_menu(page: ft.Page):
    """Função para mostrar a página do menu principal"""
    page.controls.clear()
    menu_principal_page = MenuPrincipalPage(page)
    page.add(menu_principal_page.build())
    page.update()
