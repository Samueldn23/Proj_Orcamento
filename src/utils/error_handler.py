"""Tratamento centralizado de erros"""


import flet as ft

from src.infrastructure.config.settings import settings


class ErrorHandler:
    @staticmethod
    def show_error(page: ft.Page, message: str, duration: int | None = 3000):
        """Exibe mensagem de erro na interface"""
        page.open(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=settings.THEME["ERROR_COLOR"],
                duration=duration,
            )
        )

    @staticmethod
    def log_error(error: Exception, context: str = ""):
        """Registra erro no log"""
        print(f"Erro em {context}: {error!s}")
        # Aqui você pode adicionar integração com sistema de logs
