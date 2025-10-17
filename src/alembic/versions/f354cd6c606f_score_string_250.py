from alembic import op

# revision identifiers, used by Alembic.
revision = 'f354cd6c606f'
down_revision = 'c8708b56e565'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # MySQL: изменить тип колонки на VARCHAR(250)
    op.execute("ALTER TABLE matches_table MODIFY COLUMN score VARCHAR(250) NOT NULL;")

def downgrade() -> None:
    # вернуть прежний размер (пример: VARCHAR(10))
    op.execute("ALTER TABLE matches_table MODIFY COLUMN score VARCHAR(10) NOT NULL;")
