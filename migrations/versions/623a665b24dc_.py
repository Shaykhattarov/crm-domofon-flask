"""empty message

Revision ID: 623a665b24dc
Revises: 2cfb489481e5
Create Date: 2023-05-17 16:15:28.977772

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '623a665b24dc'
down_revision = '2cfb489481e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'address', ['address_id'], ['id'])
        batch_op.drop_column('address')
        batch_op.drop_column('apartment')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('apartment', mysql.VARCHAR(collation='utf8mb4_general_ci', length=200), nullable=False))
        batch_op.add_column(sa.Column('address', mysql.VARCHAR(collation='utf8mb4_general_ci', length=500), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('address_id')

    # ### end Alembic commands ###
