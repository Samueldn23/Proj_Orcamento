"""Script para executar todas as migrações"""

from src.infrastructure.database.migrations.create_tables import create_clients_table
from src.infrastructure.database.migrations.update_cascade_delete import update_cascade_delete


def run_migrations():
    """Executa todas as migrações"""
    print("🚀 Iniciando migrações...")

    # Lista de funções de migração
    migrations = [
        create_clients_table,
        update_cascade_delete,
        # Adicione outras funções de migração aqui
    ]

    # Executa cada migração
    for migration in migrations:
        migration()

    print("✨ Migrações concluídas!")


if __name__ == "__main__":
    run_migrations()
