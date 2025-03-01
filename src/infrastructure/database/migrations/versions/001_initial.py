"""Initial migration

Revision ID: 001_initial
Create Date: 2024-01-23 13:25:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Verifica se a tabela existe
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Cria ou atualiza a tabela paredes
    if 'paredes' not in inspector.get_table_names():
        op.create_table(
            'paredes',
            sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
            sa.Column('orcamento_id', sa.BigInteger(), nullable=False),
            sa.Column('altura', sa.Numeric(10, 2), nullable=False),
            sa.Column('comprimento', sa.Numeric(10, 2), nullable=False),
            sa.Column('area', sa.Numeric(10, 2), nullable=False),
            sa.Column('valor_m2', sa.Numeric(10, 2), nullable=False),
            sa.Column('tipo_tijolo', sa.String(100), nullable=False),
            sa.Column('quantidade_tijolos', sa.BigInteger(), nullable=False),
            sa.Column('custo_tijolos', sa.Numeric(10, 2), nullable=False),
            sa.Column('custo_mao_obra', sa.Numeric(10, 2), nullable=False),
            sa.Column('custo_total', sa.Numeric(10, 2), nullable=False),
            sa.ForeignKeyConstraint(['orcamento_id'], ['orcamentos.id'], ondelete='CASCADE'),
        )
    else:
        # Se a tabela já existe, adiciona as novas colunas
        existing_columns = [c['name'] for c in inspector.get_columns('paredes')]
        new_columns = {
            'area': sa.Numeric(10, 2),
            'tipo_tijolo': sa.String(100),
            'quantidade_tijolos': sa.BigInteger(),
            'custo_tijolos': sa.Numeric(10, 2),
            'custo_mao_obra': sa.Numeric(10, 2),
            'custo_total': sa.Numeric(10, 2)
        }

        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                op.add_column('paredes', sa.Column(col_name, col_type, nullable=False, server_default='0'))
                if col_name == 'tipo_tijolo':
                    op.alter_column('paredes', col_name, server_default=None)
                else:
                    op.alter_column('paredes', col_name, server_default=None)


def downgrade() -> None:
    op.drop_table('paredes')
