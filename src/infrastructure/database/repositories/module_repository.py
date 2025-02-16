"""Repositório de módulos"""

from typing import Optional, List, Dict, Any  # noqa: F401
from ..models.module import Module  # noqa: F401
from ..connections.postgres import postgres
from ..connections.supabase import supabase


class ModuleRepository:
    """Repositório para operações com módulos"""

    def __init__(self):
        self.db = postgres
        self.supabase = supabase.client

    def get_modules(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtém os módulos do usuário"""
        try:
            response = (
                self.supabase.table("modulos")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao obter módulos: {e}")
            return []

    def create_default_modules(self, user_id: str, user_name: str) -> bool:
        """Cria os módulos padrão para um novo usuário"""
        try:
            response = (
                self.supabase.table("modulos")
                .insert(
                    {
                        "user_id": user_id,
                        "user_name": user_name,
                        "parede": True,
                        "contrapiso": False,
                        "eletrica": False,
                        "fundacao": False,
                        "laje": False,
                        "telhado": False,
                    }
                )
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao criar módulos: {e}")
            return False

    def update_module(self, user_id: str, module_data: dict) -> bool:
        """Atualiza os módulos de um usuário"""
        try:
            response = (
                self.supabase.table("modulos")
                .update(module_data)
                .eq("user_id", user_id)
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao atualizar módulos: {e}")
            return False
