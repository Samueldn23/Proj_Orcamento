"""Repositório de orçamentos"""

from typing import Optional, Dict, Any  # noqa: F401
from ..models.budget import Budget
from ..connections.postgres import postgres
from ..connections.supabase import supabase


class BudgetRepository:
    """Repositório para operações com orçamentos"""

    def __init__(self):
        self.db = postgres
        self.supabase = supabase.client

    def create(
        self,
        cliente_id: int,
        data_orcamento: str,
        descricao: str,
        valor: float,
    ) -> Optional[Budget]:
        """Adiciona um novo orçamento"""
        try:
            with self.db.get_session() as session:
                budget = Budget(
                    cliente_id=cliente_id,
                    data_criacao=data_orcamento,
                    descricao=descricao,
                    valor_total=valor,
                )
                session.add(budget)
                session.commit()
                return budget
        except Exception as e:
            print(f"Erro ao criar orçamento: {e}")
            return None
