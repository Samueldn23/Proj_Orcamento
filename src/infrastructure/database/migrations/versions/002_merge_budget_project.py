"""Migração para mesclar orçamentos em projetos

Revision ID: 002_merge_budget_project
Create Date: 2024-02-25 00:15:00
"""
from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

# revision identifiers
revision: str = '002_merge_budget_project'
down_revision: Union[str, None] = '001_initial'  # Conecta com a migração anterior
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Adicionar coluna valor_total em projetos
    op.add_column('projetos', sa.Column('valor_total', sa.Numeric(10, 2), nullable=True))

    # 2. Migrar dados de orçamentos para projetos
    op.execute("""
        UPDATE projetos p
        SET valor_total = o.valor_total
        FROM orcamentos o
        WHERE p.cliente_id = o.cliente_id
    """)

    # 3. Atualizar foreign keys nas tabelas relacionadas
    tabelas = ['fundacoes', 'contrapisos', 'lajes', 'telhados', 'eletricas', 'paredes']
    
    for tabela in tabelas:
        # Renomear coluna
        op.alter_column(tabela, 'orcamento_id', new_column_name='projeto_id')
        
        # Atualizar foreign key
        op.drop_constraint(f'{tabela}_orcamento_id_fkey', tabela)
        op.create_foreign_key(
            f'{tabela}_projeto_id_fkey',
            tabela,
            'projetos',
            ['projeto_id'],
            ['id']
        )

    # 4. Remover tabela orcamentos
    op.drop_table('orcamentos')


def downgrade():
    # 1. Recriar tabela orcamentos
    op.create_table(
        'orcamentos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('cliente_id', sa.UUID(), nullable=False),
        sa.Column('valor_total', sa.Numeric(10, 2))
    )

    # 2. Reverter dados
    op.execute("""
        INSERT INTO orcamentos (cliente_id, valor_total)
        SELECT cliente_id, valor_total FROM projetos
    """)

    # 3. Reverter foreign keys
    tabelas = ['fundacoes', 'contrapisos', 'lajes', 'telhados', 'eletricas', 'paredes']
    for tabela in tabelas:
        op.drop_constraint(f'{tabela}_projeto_id_fkey', tabela)
        op.alter_column(tabela, 'projeto_id', new_column_name='orcamento_id')
        op.create_foreign_key(
            f'{tabela}_orcamento_id_fkey',
            tabela,
            'orcamentos',
            ['orcamento_id'],
            ['id']
        )

    # 4. Remover coluna valor_total de projetos
    op.drop_column('projetos', 'valor_total')
