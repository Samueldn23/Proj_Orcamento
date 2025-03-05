"""Script para remover colunas de autenticação da tabela usuarios"""

import os

from sqlalchemy import text

from src.infrastructure.database.connections.postgres import postgres


def remove_auth_columns():
    """Remove as colunas de autenticação (email e password_hash) da tabela usuarios"""
    print("Iniciando remoção das colunas de autenticação...")

    # Caminho para o script SQL
    script_path = os.path.join("src", "infrastructure", "database", "migrations", "sql", "remove_auth_columns.sql")

    # Verificar se o arquivo existe
    if not os.path.exists(script_path):
        print(f"Arquivo SQL não encontrado: {script_path}")
        return

    # Ler o conteúdo do script SQL
    with open(script_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    # Executar o script SQL
    try:
        with postgres.get_session() as session:
            # Verificar se as colunas existem antes de tentar removê-las
            columns = session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'usuarios';")).fetchall()

            column_names = [col[0] for col in columns]

            if "email" in column_names or "password_hash" in column_names:
                print(f"Colunas encontradas para remoção: {[col for col in column_names if col in ['email', 'password_hash']]}")

                # Executar o script SQL
                session.execute(text(sql_script))
                session.commit()
                print("Colunas removidas com sucesso!")
            else:
                print("As colunas 'email' e 'password_hash' já foram removidas ou não existem.")

    except Exception as e:
        print(f"Erro ao remover colunas: {e}")


if __name__ == "__main__":
    remove_auth_columns()
