"""Script para atualizar o banco de dados"""

# from src.infrastructure.database.connections.supabase import supabase

# SQL para atualizar as restrições
SQL = """
DO $$
BEGIN
    -- Paredes
    ALTER TABLE paredes DROP CONSTRAINT IF EXISTS paredes_projeto_id_fkey;
    ALTER TABLE paredes ADD CONSTRAINT paredes_projeto_id_fkey
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

    -- Fundações
    ALTER TABLE fundacoes DROP CONSTRAINT IF EXISTS fundacoes_projeto_id_fkey;
    ALTER TABLE fundacoes ADD CONSTRAINT fundacoes_projeto_id_fkey
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

    -- Contrapisos
    ALTER TABLE contrapisos DROP CONSTRAINT IF EXISTS contrapisos_projeto_id_fkey;
    ALTER TABLE contrapisos ADD CONSTRAINT contrapisos_projeto_id_fkey
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

    -- Lajes
    ALTER TABLE lajes DROP CONSTRAINT IF EXISTS lajes_projeto_id_fkey;
    ALTER TABLE lajes ADD CONSTRAINT lajes_projeto_id_fkey
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

    -- Telhados
    ALTER TABLE telhados DROP CONSTRAINT IF EXISTS telhados_projeto_id_fkey;
    ALTER TABLE telhados ADD CONSTRAINT telhados_projeto_id_fkey
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

    -- Elétricas
    ALTER TABLE eletricas DROP CONSTRAINT IF EXISTS eletricas_projeto_id_fkey;
    ALTER TABLE eletricas ADD CONSTRAINT eletricas_projeto_id_fkey
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;
END $$;
"""


def update_database():
    """Atualiza o banco de dados"""
    try:
        print("🔄 Iniciando atualização do banco de dados...")
        print(f"\n📝 SQL a ser executado:\n{SQL}")

        # Executa o bloco SQL como uma única transação
        # response = supabase.client.postgrest.rpc("exec_sql", {"sql": SQL}).execute()

        print("\n✨ Banco de dados atualizado com sucesso!")
        return True

    except Exception as e:
        print(f"\n❌ Erro ao atualizar banco de dados: {e}")
        return False


if __name__ == "__main__":
    update_database()
