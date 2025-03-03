"""Script para executar todas as migrações"""

from create_tables import create_clients_table


def run_migrations():
    """Executa todas as migrações"""
    print("🚀 Iniciando migrações...")

    # Lista de funções de migração
    migrations = [
        create_clients_table,
        # Adicione outras funções de migração aqui
    ]

    # Executa cada migração
    for migration in migrations:
        migration()

    print("✨ Migrações concluídas!")


if __name__ == "__main__":
    run_migrations()
