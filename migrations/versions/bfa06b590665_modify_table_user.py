"""modify table user

Revision ID: bfa06b590665
Revises: 05ffdd5f3eba
Create Date: 2023-03-23 12:31:01.730877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfa06b590665'
down_revision = '05ffdd5f3eba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'roles', 'users', ['user_id'], ['id'])
    op.drop_constraint('users_role_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_role_fkey', 'users', 'roles', ['role'], ['id'])
    op.drop_constraint(None, 'roles', type_='foreignkey')
    op.drop_column('roles', 'user_id')
    # ### end Alembic commands ###