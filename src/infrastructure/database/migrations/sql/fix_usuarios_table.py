"""Script para corrigir a tabela usuarios"""

from sqlalchemy import text

from src.infrastructure.database.connections.postgres import postgres


def fix_usuarios_table():
    """Verifica e corrige a estrutura da tabela usuarios"""
    with postgres.get_session() as session:
        # Verificar se as colunas existem
        columns = session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'usuarios';")).fetchall()

        column_names = [col[0] for col in columns]
        print(f"Colunas existentes: {column_names}")

        # Adicionar colunas se não existirem
        if "email" not in column_names:
            print("Adicionando coluna 'email'...")
            session.execute(text("ALTER TABLE usuarios ADD COLUMN email VARCHAR(255) UNIQUE;"))

        if "password_hash" not in column_names:
            print("Adicionando coluna 'password_hash'...")
            session.execute(text("ALTER TABLE usuarios ADD COLUMN password_hash VARCHAR(255);"))

        # Atualizar registros existentes com valores padrão
        print("Atualizando registros existentes...")

        # Obter todos os usuários sem email
        users_without_email = session.execute(text("SELECT user_id FROM usuarios WHERE email IS NULL;")).fetchall()

        for user in users_without_email:
            user_id = user[0]
            # Gerar um email padrão baseado no ID do usuário
            default_email = f"user_{user_id}@example.com"
            default_password = "password123"  # Senha padrão temporária

            # Atualizar o registro
            session.execute(
                text("UPDATE usuarios SET email = :email, password_hash = :password WHERE user_id = :user_id"),
                {"email": default_email, "password": default_password, "user_id": user_id},
            )
            print(f"Atualizado usuário {user_id} com email padrão {default_email}")

        # Definir colunas como NOT NULL
        session.execute(text("ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL;"))
        session.execute(text("ALTER TABLE usuarios ALTER COLUMN password_hash SET NOT NULL;"))

        session.commit()
        print("Tabela 'usuarios' corrigida com sucesso!")


if __name__ == "__main__":
    fix_usuarios_table()
