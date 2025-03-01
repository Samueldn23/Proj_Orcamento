"""Configurações centralizadas da aplicação"""

import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings:
    """Configurações globais da aplicação"""

    # Informações básicas
    APP_NAME = "Sistema de Orçamentos"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Configurações do banco de dados PostgreSQL
    DB_USER = os.getenv("DB_USER")
    DB_PASS = quote(os.getenv("DB_PASS"))
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    # Configurações Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    @property
    def DATABASE_URL(self) -> str:
        """Retorna a URL de conexão PostgreSQL"""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"
        )

    # Configurações de tema
    THEME = {
        "PRIMARY_COLOR": "#1565C0",
        "SECONDARY_COLOR": "#FFA726",
        "ERROR_COLOR": "#D32F2F",
        "SUCCESS_COLOR": "#2E7D32",
        "WARNING_COLOR": "#ED6C02",
    }


settings = Settings()
