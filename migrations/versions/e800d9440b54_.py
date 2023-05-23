"""empty message

Revision ID: e800d9440b54
Revises: f8969f3fa0b4
Create Date: 2023-05-23 21:03:12.704191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e800d9440b54'
down_revision = 'f8969f3fa0b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.alter_column('apartment',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.drop_constraint('address_ibfk_5', type_='foreignkey')
        batch_op.drop_constraint('address_ibfk_7', type_='foreignkey')
        batch_op.drop_constraint('address_ibfk_4', type_='foreignkey')
        batch_op.create_foreign_key(None, 'tariff', ['tariff_id'], ['id'])
        batch_op.create_foreign_key(None, 'equipment', ['equipment_id'], ['id'])
        batch_op.create_foreign_key(None, 'district', ['district_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('address_ibfk_4', 'district', ['district_id'], ['id'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('address_ibfk_7', 'equipment', ['equipment_id'], ['id'], onupdate='RESTRICT', ondelete='SET NULL')
        batch_op.create_foreign_key('address_ibfk_5', 'tariff', ['tariff_id'], ['id'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.alter_column('apartment',
               existing_type=sa.String(length=200),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###