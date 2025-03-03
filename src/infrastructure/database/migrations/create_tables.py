"""Script para criar tabelas no Supabase"""

from pathlib import Path

from src.infrastructure.database.connections.supabase import supabase

# Diretório base das migrações
MIGRATIONS_DIR = Path(__file__).parent
SQL_DIR = MIGRATIONS_DIR / "sql"


def read_sql_file(filename: str) -> str:
    """Lê um arquivo SQL do diretório de migrações"""
    with open(SQL_DIR / filename, encoding="utf-8") as file:
        return file.read()


def create_clients_table():
    """Cria a tabela de clientes no Supabase"""
    try:
        # Lê o SQL do arquivo
        sql = read_sql_file("create_clients_table.sql")

        # Executar o SQL via cliente Supabase
        supabase.client.query(sql).execute()
        print("✅ Tabela 'clientes' criada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar tabela 'clientes': {e}")


if __name__ == "__main__":
    create_clients_table()
