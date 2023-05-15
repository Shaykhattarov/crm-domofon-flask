"""add district

Revision ID: da321431d819
Revises: fd0acc5e133b
Create Date: 2023-05-09 02:07:26.837010

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'da321431d819'
down_revision = 'fd0acc5e133b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('district',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('district_id', sa.Integer(), nullable=True))
        batch_op.alter_column('apartment',
               existing_type=mysql.VARCHAR(collation='utf8mb4_general_ci', length=200),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.create_foreign_key(None, 'tariff', ['tariff_id'], ['id'])
        batch_op.create_foreign_key(None, 'district', ['district_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('apartment',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(collation='utf8mb4_general_ci', length=200),
               existing_nullable=False)
        batch_op.drop_column('district_id')

    op.drop_table('district')
    # ### end Alembic commands ###