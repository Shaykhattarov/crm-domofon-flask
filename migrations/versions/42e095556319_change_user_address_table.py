"""change user_address table

Revision ID: 42e095556319
Revises: 219ba7becb11
Create Date: 2023-04-19 19:46:14.879860

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '42e095556319'
down_revision = '219ba7becb11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active_sub', sa.Integer(), nullable=False))
        batch_op.alter_column('payment_date',
               existing_type=mysql.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.alter_column('end_date',
               existing_type=mysql.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.drop_column('active_payment')

    with op.batch_alter_table('user_address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'address', ['address_id'], ['id'])
        batch_op.drop_column('house')
        batch_op.drop_column('front_door')
        batch_op.drop_column('street')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('street', mysql.VARCHAR(collation='utf8mb4_general_ci', length=2000), nullable=False))
        batch_op.add_column(sa.Column('front_door', mysql.VARCHAR(collation='utf8mb4_general_ci', length=200), nullable=True))
        batch_op.add_column(sa.Column('house', mysql.VARCHAR(collation='utf8mb4_general_ci', length=200), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('address_id')

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active_payment', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.alter_column('end_date',
               existing_type=sa.Date(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
        batch_op.alter_column('payment_date',
               existing_type=sa.Date(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
        batch_op.drop_column('active_sub')

    # ### end Alembic commands ###
