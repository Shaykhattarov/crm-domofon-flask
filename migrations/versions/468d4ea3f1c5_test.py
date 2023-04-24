"""test

Revision ID: 468d4ea3f1c5
Revises: 8b9df27617b5
Create Date: 2023-04-23 16:30:28.147213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '468d4ea3f1c5'
down_revision = '8b9df27617b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.alter_column('tariff_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('end_date',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.create_foreign_key(None, 'payment', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('user_ibfk_3', 'payment', ['payment_id'], ['id'])

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_status', mysql.VARCHAR(collation='utf8mb4_general_ci', length=200), nullable=True))
        batch_op.add_column(sa.Column('payment_date', sa.DATE(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('end_date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('tariff_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.drop_column('start_date')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###