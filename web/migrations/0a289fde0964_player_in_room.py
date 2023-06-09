"""player in_room

Revision ID: 0a289fde0964
Revises: f2abefc0b53d
Create Date: 2023-06-07 17:52:22.801348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a289fde0964'
down_revision = 'f2abefc0b53d'
branch_labels = ()
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('in_room', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('player', 'in_room')
    # ### end Alembic commands ###