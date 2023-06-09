"""empty message

Revision ID: b52ae8eecf8a
Revises: 2ec5848db061
Create Date: 2023-05-10 17:15:51.378606

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b52ae8eecf8a'
down_revision = '2ec5848db061'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_on_server', sa.String(length=3000), nullable=False))
        batch_op.drop_column('path')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('path', mysql.VARCHAR(collation='utf8mb4_general_ci', length=3000), nullable=True))
        batch_op.drop_column('name_on_server')

    # ### end Alembic commands ###
