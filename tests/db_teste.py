"""Importação de bibliotecas e módulos necessários"""

import flet as ft
from sqlalchemy.sql import text

import custom.button as clk
from custom.styles_utils import get_style_manager
from models.db import Session

import tests.db_n_teste as tst

gsm = get_style_manager()


def testar_conecxao(page: ft.Page):
    """Função para testar a conexão com o banco de dados"""
    page.controls.clear()
    page.title = "Teste de Conexão com o Banco de Dados"

    def test_connection(event=None):  # pylint: disable=unused-argument
        """Função para testar a conexão com o banco de dados"""

        try:
            session = Session()
            session.execute(text("SELECT 1"))  # Usando text() para a consulta
            print("Conexão com o Supabase bem-sucedida!")
        except ValueError as e:
            print(f"Erro ao conectar: {e}")
        finally:
            session.close()

    btn_teste = gsm.create_button(
        text="Testar Conexão",
        on_click=test_connection,
        icon=ft.icons.CHECK_CIRCLE_OUTLINE,
        hover_color=gsm.colors.SECONDARY,
    )
    btn_teste2 = gsm.create_button(
        text="Testar Conexão",
        on_click=tst.testar_conexao(),
        icon=ft.icons.CHECK_CIRCLE_OUTLINE,
        hover_color=gsm.colors.SECONDARY,
    )

    btn_voltar = gsm.create_button(
        text="Voltar",
        on_click=lambda _: clk.Voltar.principal(page),
        icon=ft.icons.ARROW_BACK_IOS_NEW,
        hover_color=gsm.colors.VOLTAR,
    )

    page.add(btn_teste, btn_teste2, btn_voltar)
