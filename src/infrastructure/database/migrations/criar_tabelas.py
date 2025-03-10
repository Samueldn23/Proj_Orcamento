"""Script para criar tabelas no Supabase"""

from pathlib import Path

from sqlalchemy import text

from src.infrastructure.database.connections.supabase import supabase

from ..connections.postgres import postgres

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


def update_usuarios_table():
    """Atualiza a tabela de usuários"""
    try:
        with postgres.get_session() as session:
            # Lê o SQL do arquivo
            sql = read_sql_file("update_usuarios_table.sql")
            # Executar o SQL
            session.execute(text(sql))
            session.commit()
            print("✅ Tabela 'usuarios' atualizada com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao atualizar tabela 'usuarios': {e}")
        return False


def update_paredes_table():
    """Atualiza a tabela de paredes"""
    try:
        with postgres.get_session() as session:
            # Lê o SQL do arquivo
            sql = read_sql_file("update_paredes_table.sql")
            # Executar o SQL
            session.execute(text(sql))
            session.commit()
            print("✅ Tabela 'paredes' atualizada com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao atualizar tabela 'paredes': {e}")
        return False


def update_lajes_table():
    """Atualiza a tabela de lajes"""
    try:
        with postgres.get_session() as session:
            # Lê o SQL do arquivo
            sql = read_sql_file("lajes.sql")
            # Executar o SQL
            session.execute(text(sql))
            session.commit()
            print("✅ Tabela 'lajes' atualizada com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao atualizar tabela 'lajes': {e}")
        return False


if __name__ == "__main__":
    create_clients_table()
    update_usuarios_table()
    update_paredes_table()
    update_lajes_table()
