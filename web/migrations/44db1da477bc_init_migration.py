"""init migration

Revision ID: 44db1da477bc
Revises: 
Create Date: 2023-06-05 22:58:40.285464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44db1da477bc'
down_revision = None
branch_labels = ('default',)
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    op.drop_table('player')
    op.drop_table('game')
    # ### end Alembic commands ###
