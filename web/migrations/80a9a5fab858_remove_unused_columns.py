"""remove unused columns

Revision ID: 80a9a5fab858
Revises: 02e1b754c22d
Create Date: 2023-06-11 17:19:02.490808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80a9a5fab858'
down_revision = '02e1b754c22d'
branch_labels = ()
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'in_progress')
    op.drop_column('player', 'in_room')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('in_room', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('game', sa.Column('in_progress', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
