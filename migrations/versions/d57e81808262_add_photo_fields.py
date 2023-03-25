"""add photo fields

Revision ID: d57e81808262
Revises: 7a624fb396c5
Create Date: 2023-03-23 18:55:05.403577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd57e81808262'
down_revision = '7a624fb396c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_profile_photos_id', table_name='profile_photos')
    op.drop_table('profile_photos')
    op.add_column('profiles', sa.Column('photo', sa.LargeBinary(), nullable=True))
    op.add_column('profiles', sa.Column('position', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'position')
    op.drop_column('profiles', 'photo')
    op.create_table('profile_photos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('data', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='profile_photos_pkey')
    )
    op.create_index('ix_profile_photos_id', 'profile_photos', ['id'], unique=False)
    # ### end Alembic commands ###
