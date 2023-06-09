"""add count tables

Revision ID: 05ffdd5f3eba
Revises: 7e84c9a1dbe4
Create Date: 2023-03-22 23:39:55.113423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ffdd5f3eba'
down_revision = '7e84c9a1dbe4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ratings_stars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ratings_stars_id'), 'ratings_stars', ['id'], unique=False)
    op.create_table('ratings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('star', sa.Integer(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.ForeignKeyConstraint(['star'], ['ratings_stars.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ratings_id'), 'ratings', ['id'], unique=False)
    op.add_column('profiles', sa.Column('views', sa.Integer(), nullable=True))
    op.add_column('profiles', sa.Column('count_student', sa.Integer(), nullable=True))
    op.add_column('profiles', sa.Column('count_course', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'count_course')
    op.drop_column('profiles', 'count_student')
    op.drop_column('profiles', 'views')
    op.drop_index(op.f('ix_ratings_id'), table_name='ratings')
    op.drop_table('ratings')
    op.drop_index(op.f('ix_ratings_stars_id'), table_name='ratings_stars')
    op.drop_table('ratings_stars')
    # ### end Alembic commands ###
