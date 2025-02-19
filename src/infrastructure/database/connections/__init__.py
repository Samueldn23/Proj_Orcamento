"""Módulo de conexões com banco de dados"""

from .postgres import PostgresConnection
from .supabase import SupabaseConnection

__all__ = ["PostgresConnection", "SupabaseConnection"]
