"""empty message

Revision ID: a3dca033253e
Revises: 7c6d90394650
Create Date: 2023-04-24 02:27:02.234865

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a3dca033253e'
down_revision = '7c6d90394650'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=500), nullable=False))
        batch_op.drop_constraint('application_ibfk_1', type_='foreignkey')
        batch_op.drop_column('address_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('application_ibfk_1', 'address', ['address_id'], ['id'])
        batch_op.drop_column('address')

    # ### end Alembic commands ###
