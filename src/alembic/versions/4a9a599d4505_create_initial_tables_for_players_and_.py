"""Create initial tables for players and matches

Revision ID: 4a9a599d4505
Revises:
Create Date: 2025-09-28 22:21:58.010766
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4a9a599d4505'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create players table
    op.create_table(
        'players_table',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=30), nullable=False),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_general_ci'
    )

    # create matches table
    op.create_table(
        'matches_table',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(length=36), nullable=False, unique=True),
        sa.Column('player1_id', sa.Integer(), sa.ForeignKey('players_table.id'), nullable=True),
        sa.Column('player2_id', sa.Integer(), sa.ForeignKey('players_table.id'), nullable=True),
        sa.Column('winner', sa.Integer(), sa.ForeignKey('players_table.id'), nullable=True),
        # создаём score коротким (чтобы последующие миграции могли изменить длину)
        sa.Column('score', sa.String(length=10), nullable=False),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_general_ci'
    )


def downgrade() -> None:
    # drop matches first due to FKs
    op.drop_table('matches_table')
    op.drop_table('players_table')
