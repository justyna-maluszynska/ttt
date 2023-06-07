"""game player m2m

Revision ID: f2abefc0b53d
Revises: 0535f157b81a
Create Date: 2023-06-07 00:27:20.024964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2abefc0b53d'
down_revision = '0535f157b81a'
branch_labels = ()
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player_game',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('player_id', 'game_id')
    )
    op.add_column('game', sa.Column('in_progress', sa.Boolean(), nullable=True))
    op.drop_constraint('game_winner_fkey', 'game', type_='foreignkey')
    op.drop_constraint('game_loser_fkey', 'game', type_='foreignkey')
    op.drop_constraint('game_player_1_fkey', 'game', type_='foreignkey')
    op.drop_constraint('game_player_2_fkey', 'game', type_='foreignkey')
    op.drop_column('game', 'winner')
    op.drop_column('game', 'player_1')
    op.drop_column('game', 'loser')
    op.drop_column('game', 'player_2')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('player_2', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('game', sa.Column('loser', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('game', sa.Column('player_1', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('game', sa.Column('winner', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('game_player_2_fkey', 'game', 'player', ['player_2'], ['id'])
    op.create_foreign_key('game_player_1_fkey', 'game', 'player', ['player_1'], ['id'])
    op.create_foreign_key('game_loser_fkey', 'game', 'player', ['loser'], ['id'])
    op.create_foreign_key('game_winner_fkey', 'game', 'player', ['winner'], ['id'])
    op.drop_column('game', 'in_progress')
    op.drop_table('player_game')
    # ### end Alembic commands ###
