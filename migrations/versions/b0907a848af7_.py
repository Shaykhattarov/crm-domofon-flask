"""empty message

Revision ID: b0907a848af7
Revises: 5495265fb8b1
Create Date: 2023-04-19 16:01:00.122269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0907a848af7'
down_revision = '5495265fb8b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tariff_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('equipment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'equipment', ['equipment_id'], ['id'])
        batch_op.create_foreign_key(None, 'tariff', ['tariff_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('equipment_id')
        batch_op.drop_column('tariff_id')

    # ### end Alembic commands ###
