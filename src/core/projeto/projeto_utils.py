"""Utilitários compartilhados entre os módulos de projeto"""

import flet as ft
from sqlalchemy import text

from src.infrastructure.database.connections.postgres import postgres
from src.infrastructure.database.repositories import RepositorioProjeto


def atualizar_custo_estimado(projeto_id: int) -> None:
    """Atualiza o custo estimado do projeto"""
    try:
        with postgres.session_scope() as session:
            # Calcula soma dos custos de todas as construções
            sql = text("""
                SELECT COALESCE(SUM(custo_total), 0) as total FROM (
                    SELECT custo_total FROM paredes WHERE projeto_id = :pid
                    UNION ALL
                    SELECT custo_total FROM lajes WHERE projeto_id = :pid
                ) as custos
            """)

            result = session.execute(sql, {"pid": projeto_id})
            custo_total = result.scalar() or 0

            # Atualiza o projeto usando o repositório
            repo = RepositorioProjeto()
            repo.atualizar_valor_total(projeto_id, custo_total)

    except Exception as e:
        print(f"Erro ao atualizar custo estimado: {e}")


def mostrar_mensagem(page: ft.Page, mensagem: str, cor: str) -> None:
    """Exibe uma mensagem na snackbar"""
    if hasattr(page, "snack_bar"):
        page.snack_bar = ft.SnackBar(content=ft.Text(mensagem), bgcolor=cor)
        page.snack_bar.open = True
        page.update()
