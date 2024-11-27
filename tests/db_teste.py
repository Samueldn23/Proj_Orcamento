"""Módulo para testar a conexão com o banco de dados"""

import flet as ft
from sqlalchemy.sql import text

from custom.button import Voltar
from custom.styles_utils import get_style_manager
from models.db import obter_supabase_client
from models.db_sql import Session


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

    def test_db_query(event=None):  # pylint: disable=unused-argument
        """Função para testar a consulta na tabela 'clientes'"""
        try:
            response = obter_supabase_client().table("clientes").select("*").execute()
            clientes = response.data
            dados_tratados = tratar_dados(clientes)  # Tratar os dados
            exibir_dados(dados_tratados)  # Exibir os dados tratados
        except Exception as e:  # pylint: disable=broad-except
            print(f"Erro ao consultar a tabela: {e}")

    def tratar_dados(clientes):
        """Trata os dados da lista de clientes, removendo entradas vazias e formatando o output."""
        dados_tratados = []

        for cliente in clientes:
            # Remover campos vazios ou nulos
            if cliente["endereco"] is None:
                cliente["endereco"] = "Não especificado"
            if cliente["cidade"] is None:
                cliente["cidade"] = "Não especificado"
            if cliente["estado"] is None:
                cliente["estado"] = "Não especificado"
            if cliente["cep"] is None:
                cliente["cep"] = "Não especificado"
            if cliente["bairro"] is None:
                cliente["bairro"] = "Não especificado"
            if cliente["numero"] is None:
                cliente["numero"] = "Não especificado"

            # Adicionar cliente tratado à lista
            dados_tratados.append(cliente)

        return dados_tratados

    def exibir_dados(clientes):
        """Exibe os dados formatados na saída padrão."""
        for cliente in clientes:
            print(f"ID: {cliente['id']}")
            print(f"Nome: {cliente['nome']}")
            print(f"CPF: {cliente['cpf']}")
            print(f"Telefone: {cliente['telefone']}")
            print(f"Email: {cliente['email']}")
            print(f"Endereço: {cliente['endereco']}")
            print(f"Cidade: {cliente['cidade']}")
            print(f"Estado: {cliente['estado']}")
            print(f"CEP: {cliente['cep']}")
            print(f"Bairro: {cliente['bairro']}")
            print(f"Número: {cliente['numero']}")
            print("-" * 40)

    page.add(
        gsm.create_button(
            text="Testar Conexão",
            on_click=test_connection,
            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
            hover_color=gsm.colors.SECONDARY,
        ),
        gsm.create_button(
            text="DB Teste",
            on_click=test_db_query,  # Chamar a nova função
            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
        ),
        gsm.create_button(
            text="Voltar",
            on_click=lambda _: Voltar.principal(page),
            icon=ft.icons.ARROW_BACK_IOS_NEW,
            hover_color=gsm.colors.VOLTAR,
        ),
    )
