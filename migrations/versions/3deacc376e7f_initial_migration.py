"""Initial Migration

Revision ID: 3deacc376e7f
Revises: 35f184ca9752
Create Date: 2020-12-05 10:44:45.695502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3deacc376e7f'
down_revision = '35f184ca9752'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('profile_pic_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic_path')
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###
