"""Aplicativo de Orçamentos com Flet e SQLAlchemy, sem autenticação de usuários. app.py"""

from typing import Optional

import flet as ft

from custom.styles_utils import get_style_manager
from menu import mostrar_menu

gsm = get_style_manager()


class OrcamentoApp:
    """Classe principal do aplicativo de orçamentos"""

    def __init__(self):
        self.page: Optional[ft.Page] = None
        self.gsm = get_style_manager()

    def configure_page(self, page: ft.Page):
        """Configura a página principal do aplicativo"""
        self.page = page
        self.gsm.apply_theme(page)
        page.title = "App de Orçamento"
        page.window.min_width = 450  # Largura mínima para responsividade
        page.update()

    def show_welcome_message(self):
        """Exibe a mensagem de boas-vindas"""
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Bem-vindo ao Sistema de Orçamento",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE,
                        ),
                        ft.Text(
                            "Faça login para continuar",
                            size=16,
                            color=ft.colors.GREY_700,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=20,
                alignment=ft.alignment.center,
            )
        )

    def main(self, page: ft.Page):
        """Função principal do aplicativo"""
        try:
            self.configure_page(page)
            self.show_welcome_message()
            mostrar_menu(page)
            page.update()
        except ValueError as e:
            error_message = f"Erro ao inicializar o aplicativo: {str(e)}"
            page.add(ft.Text(error_message, color=ft.colors.RED_600))
            page.update()
            print(error_message)


def start_app():
    """Função para iniciar o aplicativo"""
    try:
        app = OrcamentoApp()
        ft.app(target=app.main)
    except ValueError as e:
        print(f"Erro fatal ao iniciar o aplicativo: {e}")


if __name__ == "__main__":
    start_app()
