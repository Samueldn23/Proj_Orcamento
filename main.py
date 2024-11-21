import flet as ft
from typing import Optional
from user.login import mostrar_login
from models.db import criar_tabelas
from custom.styles_utils import get_style_manager

gsm = get_style_manager()

class OrcamentoApp:
    """Classe principal do aplicativo de orçamentos"""

    def __init__(self):
        self.tabelas_criadas: bool = False
        self.page: Optional[ft.Page] = None

    def initialize_database(self):
        """Inicializa o banco de dados se necessário"""
        if not self.tabelas_criadas:
            try:
                criar_tabelas()
                self.tabelas_criadas = True
            except Exception as e:
                print(f"Erro ao criar tabelas: {e}")
                raise

    def configure_page(self, page: ft.Page):
        """Configura a página principal do aplicativo"""
        self.page = page
        gsm.apply_theme(page)
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
            self.initialize_database()
            self.configure_page(page)
            self.show_welcome_message()
            mostrar_login(page)
            page.update()
        except Exception as e:
            error_message = f"Erro ao inicializar o aplicativo: {str(e)}"
            page.add(ft.Text(error_message, color=ft.colors.RED_600))
            page.update()
            print(error_message)


def start_app():
    """Função para iniciar o aplicativo"""
    try:
        app = OrcamentoApp()
        ft.app(target=app.main)
    except Exception as e:
        print(f"Erro fatal ao iniciar o aplicativo: {e}")


if __name__ == "__main__":
    start_app()
