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


def update_usuarios_table():
    """Atualiza a tabela de usuários com os campos de autenticação"""
    try:
        # Lê o SQL do arquivo
        sql = read_sql_file("update_usuarios_table.sql")

        # Executar o SQL via cliente Supabase
        supabase.client.query(sql).execute()
        print("✅ Tabela 'usuarios' atualizada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao atualizar tabela 'usuarios': {e}")


def update_paredes_table():
    """Atualiza a tabela paredes para adicionar ON DELETE CASCADE"""
    try:
        # SQL para atualizar a restrição de chave estrangeira
        sql = """
        ALTER TABLE paredes DROP CONSTRAINT IF EXISTS paredes_projeto_id_fkey;
        ALTER TABLE paredes ADD CONSTRAINT paredes_projeto_id_fkey
        FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;
        """

        # Executar o SQL via cliente Supabase
        supabase.client.query(sql).execute()
        print("✅ Tabela 'paredes' atualizada com sucesso com ON DELETE CASCADE!")

    except Exception as e:
        print(f"❌ Erro ao atualizar tabela 'paredes': {e}")


if __name__ == "__main__":
    create_clients_table()
    update_usuarios_table()
    update_paredes_table()
