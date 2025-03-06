"""Script para atualizar as restrições de chave estrangeira no Supabase"""

from pathlib import Path

from src.infrastructure.database.connections.supabase import supabase

# Diretório base das migrações
MIGRATIONS_DIR = Path(__file__).parent
SQL_DIR = MIGRATIONS_DIR / "sql"


def read_sql_file(filename: str) -> str:
    """Lê um arquivo SQL do diretório de migrações"""
    try:
        file_path = SQL_DIR / filename
        print(f"📖 Lendo arquivo SQL: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        with open(file_path, encoding="utf-8") as file:
            content = file.read()
            print("✅ Arquivo SQL lido com sucesso!")
            return content

    except Exception as e:
        print(f"❌ Erro ao ler arquivo SQL: {e}")
        raise


def update_cascade_delete():
    """Atualiza as restrições de chave estrangeira para CASCADE DELETE"""
    print("\n🔄 Iniciando atualização das restrições de chave estrangeira...")

    try:
        # Lê o SQL do arquivo
        sql = read_sql_file("update_cascade_delete.sql")
        print("\n📝 Conteúdo SQL a ser executado:")
        print(sql)

        # Executar o SQL via cliente Supabase
        print("\n⚡ Executando SQL no Supabase...")
        result = supabase.client.query(sql).execute()
        print("\n✅ Restrições de chave estrangeira atualizadas com sucesso!")
        print(f"Resultado: {result}")

    except Exception as e:
        print(f"\n❌ Erro ao atualizar restrições: {e}")
        raise


if __name__ == "__main__":
    try:
        update_cascade_delete()
        print("\n✨ Migração concluída com sucesso!")
    except Exception as e:
        print(f"\n💥 Erro fatal durante a migração: {e}")
        raise
