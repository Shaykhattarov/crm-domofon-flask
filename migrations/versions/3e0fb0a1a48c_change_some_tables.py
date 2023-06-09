"""change some tables

Revision ID: 3e0fb0a1a48c
Revises: f91e5b604a0f
Create Date: 2023-04-18 22:15:58.869847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e0fb0a1a48c'
down_revision = 'f91e5b604a0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('individual_code', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_address', schema=None) as batch_op:
        batch_op.drop_column('individual_code')

    # ### end Alembic commands ###
