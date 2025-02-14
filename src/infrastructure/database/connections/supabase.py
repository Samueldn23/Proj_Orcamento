"""Conexão com Supabase"""

from supabase import Client, create_client
from ...config.settings import settings


class SupabaseConnection:
    """Gerenciador de conexão Supabase"""

    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa a conexão"""
        self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    @property
    def client(self) -> Client:
        """Retorna o cliente Supabase"""
        return self._client


supabase = SupabaseConnection()
