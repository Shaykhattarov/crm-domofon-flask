"""empty message

Revision ID: 28e459ca3b0f
Revises: 908a34f6e4c9
Create Date: 2023-05-05 01:38:17.534167

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '28e459ca3b0f'
down_revision = '908a34f6e4c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_address')
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('apartment', sa.String(length=200), nullable=False))
        batch_op.alter_column('front_door',
               existing_type=mysql.VARCHAR(collation='utf8mb4_general_ci', length=200),
               nullable=False)
        batch_op.drop_constraint('address_ibfk_2', type_='foreignkey')
        batch_op.drop_column('individual_code')
        batch_op.drop_column('tariff_id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_ibfk_4', type_='foreignkey')
        batch_op.create_foreign_key(None, 'address', ['address_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_ibfk_4', 'user_address', ['address_id'], ['id'])

    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tariff_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('individual_code', mysql.VARCHAR(collation='utf8mb4_general_ci', length=16), nullable=True))
        batch_op.create_foreign_key('address_ibfk_2', 'tariff', ['tariff_id'], ['id'])
        batch_op.alter_column('front_door',
               existing_type=mysql.VARCHAR(collation='utf8mb4_general_ci', length=200),
               nullable=True)
        batch_op.drop_column('apartment')

    op.create_table('user_address',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('apartment', mysql.VARCHAR(collation='utf8mb4_general_ci', length=200), nullable=True),
    sa.Column('address_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], name='user_address_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
