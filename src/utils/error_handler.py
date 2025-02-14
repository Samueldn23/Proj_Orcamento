"""Tratamento centralizado de erros"""
from typing import Optional
import flet as ft
from src.infrastructure.config.settings import settings

class ErrorHandler:
    @staticmethod
    def show_error(page: ft.Page, message: str, duration: Optional[int] = 3000):
        """Exibe mensagem de erro na interface"""
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=settings.THEME["ERROR_COLOR"],
                duration=duration
            )
        )
    
    @staticmethod
    def log_error(error: Exception, context: str = ""):
        """Registra erro no log"""
        print(f"Erro em {context}: {str(error)}")
        # Aqui você pode adicionar integração com sistema de logs 